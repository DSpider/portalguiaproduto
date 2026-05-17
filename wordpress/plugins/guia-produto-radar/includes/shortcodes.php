<?php

if (!defined('ABSPATH')) {
    exit;
}

function gpr_register_shortcodes(): void
{
    add_shortcode('guia_produto_radar', 'gpr_render_radar_shortcode');
    add_shortcode('guia_produto_ranking', 'gpr_render_ranking_shortcode');
    add_shortcode('guia_produto_tendencias', 'gpr_render_trends_shortcode');
    add_action('wp_enqueue_scripts', 'gpr_maybe_enqueue_frontend_assets');
    add_filter('wp_robots', 'gpr_noindex_radar_test_page');
}

function gpr_maybe_enqueue_frontend_assets(): void
{
    if (is_admin() || !is_singular()) {
        return;
    }

    global $post;

    if (!$post instanceof WP_Post) {
        return;
    }

    $content = $post->post_content;
    if (
        has_shortcode($content, 'guia_produto_radar')
        || has_shortcode($content, 'guia_produto_ranking')
        || has_shortcode($content, 'guia_produto_tendencias')
    ) {
        gpr_enqueue_frontend_assets();
    }
}

function gpr_enqueue_frontend_assets(): void
{
    wp_enqueue_style(
        'gpr-frontend',
        GPR_PLUGIN_URL . 'assets/css/frontend.css',
        array(),
        GPR_VERSION
    );
}

function gpr_render_fallback(string $message = ''): string
{
    gpr_enqueue_frontend_assets();

    if ('' === $message) {
        $message = 'O Radar esta temporariamente indisponivel. Tente novamente em instantes.';
    }

    return sprintf(
        '<div class="gpr-box gpr-box--fallback" role="status"><p>%s</p></div>',
        esc_html($message)
    );
}

function gpr_noindex_radar_test_page(array $robots): array
{
    if (!is_page('radar-teste')) {
        return $robots;
    }

    $robots['noindex'] = true;
    $robots['nofollow'] = true;

    return $robots;
}

function gpr_render_radar_shortcode($atts = array()): string
{
    gpr_enqueue_frontend_assets();

    $summary = gpr_get_radar_summary();
    if (is_wp_error($summary)) {
        return gpr_render_fallback();
    }

    $total_products = isset($summary['total_products']) ? absint($summary['total_products']) : 0;
    $mode = isset($summary['mode']) ? sanitize_text_field((string) $summary['mode']) : 'mock';
    $generated_at = isset($summary['generated_at']) ? sanitize_text_field((string) $summary['generated_at']) : '';
    $highlighted_products = gpr_normalize_products($summary['highlighted_products'] ?? array());

    ob_start();
    ?>
    <section class="gpr-box gpr-radar" aria-label="Guia Produto Radar">
        <header class="gpr-header">
            <h2>Guia Produto Radar</h2>
            <p><?php echo esc_html(sprintf('%d produtos monitorados. Fonte: %s.', $total_products, $mode)); ?></p>
            <?php if ('' !== $generated_at) : ?>
                <p class="gpr-meta"><?php echo esc_html('Ultima atualizacao: ' . $generated_at); ?></p>
            <?php endif; ?>
        </header>
        <?php echo gpr_render_product_list($highlighted_products, false); ?>
    </section>
    <?php
    return (string) ob_get_clean();
}

function gpr_render_ranking_shortcode($atts = array()): string
{
    gpr_enqueue_frontend_assets();

    $atts = shortcode_atts(
        array(
            'categoria' => 'tecnologia',
            'limite' => 10,
        ),
        $atts,
        'guia_produto_ranking'
    );

    $category = sanitize_key((string) $atts['categoria']);
    $limit = gpr_sanitize_limit($atts['limite']);
    $products = gpr_get_products();

    if (is_wp_error($products)) {
        return gpr_render_fallback();
    }

    $products = gpr_filter_products_by_category(gpr_normalize_products($products), $category);
    $products = gpr_sort_products_by_trend_score($products);
    $products = array_slice($products, 0, $limit);

    if (empty($products)) {
        return gpr_render_fallback('Nenhum produto encontrado para esta categoria no momento.');
    }

    ob_start();
    ?>
    <section class="gpr-box gpr-ranking" aria-label="Ranking Guia Produto">
        <header class="gpr-header">
            <h2><?php echo esc_html('Ranking: ' . $category); ?></h2>
        </header>
        <?php echo gpr_render_product_list($products, true); ?>
    </section>
    <?php
    return (string) ob_get_clean();
}

function gpr_render_trends_shortcode($atts = array()): string
{
    gpr_enqueue_frontend_assets();

    $atts = shortcode_atts(
        array(
            'limite' => 10,
        ),
        $atts,
        'guia_produto_tendencias'
    );

    $limit = gpr_sanitize_limit($atts['limite']);
    $summary = gpr_get_radar_summary();

    if (is_wp_error($summary)) {
        return gpr_render_fallback();
    }

    $products = gpr_normalize_products($summary['highlighted_products'] ?? array());
    $products = gpr_sort_products_by_trend_score($products);
    $products = array_slice($products, 0, $limit);

    if (empty($products)) {
        return gpr_render_fallback('Nenhuma tendencia disponivel no momento.');
    }

    ob_start();
    ?>
    <section class="gpr-box gpr-trends" aria-label="Tendencias Guia Produto">
        <header class="gpr-header">
            <h2>Produtos em tendencia</h2>
        </header>
        <?php echo gpr_render_product_list($products, false); ?>
    </section>
    <?php
    return (string) ob_get_clean();
}

function gpr_sanitize_limit($value): int
{
    $limit = absint($value);

    if ($limit < 1) {
        return 1;
    }

    if ($limit > 20) {
        return 20;
    }

    return $limit;
}

function gpr_normalize_products($products): array
{
    if (!is_array($products)) {
        return array();
    }

    $normalized = array();
    foreach ($products as $product) {
        if (!is_array($product)) {
            continue;
        }

        $normalized[] = array(
            'slug' => isset($product['slug']) ? sanitize_title((string) $product['slug']) : '',
            'name' => isset($product['name']) ? sanitize_text_field((string) $product['name']) : '',
            'brand' => isset($product['brand']) ? sanitize_text_field((string) $product['brand']) : '',
            'category' => isset($product['category']) ? sanitize_key((string) $product['category']) : '',
            'trend_score' => isset($product['trend_score']) ? absint($product['trend_score']) : 0,
            'confidence' => isset($product['confidence']) ? sanitize_text_field((string) $product['confidence']) : '',
        );
    }

    return $normalized;
}

function gpr_filter_products_by_category(array $products, string $category): array
{
    if ('' === $category || 'tecnologia' === $category || 'todos' === $category) {
        return $products;
    }

    return array_values(
        array_filter(
            $products,
            static function (array $product) use ($category): bool {
                return isset($product['category']) && $product['category'] === $category;
            }
        )
    );
}

function gpr_sort_products_by_trend_score(array $products): array
{
    usort(
        $products,
        static function (array $first, array $second): int {
            return ($second['trend_score'] ?? 0) <=> ($first['trend_score'] ?? 0);
        }
    );

    return $products;
}

function gpr_render_product_list(array $products, bool $ordered): string
{
    if (empty($products)) {
        return '<p class="gpr-empty">Nenhum produto disponivel no momento.</p>';
    }

    $tag = $ordered ? 'ol' : 'ul';
    $html = sprintf('<%1$s class="gpr-product-list">', esc_attr($tag));

    foreach ($products as $product) {
        $html .= '<li class="gpr-product">';
        $html .= sprintf('<strong class="gpr-product__name">%s</strong>', esc_html($product['name']));

        if (!empty($product['brand'])) {
            $html .= sprintf('<span class="gpr-product__brand">%s</span>', esc_html($product['brand']));
        }

        $html .= sprintf(
            '<span class="gpr-product__score">%s</span>',
            esc_html('Trend score: ' . absint($product['trend_score']))
        );

        if (!empty($product['confidence'])) {
            $html .= sprintf(
                '<span class="gpr-product__meta">%s</span>',
                esc_html('Confianca: ' . $product['confidence'])
            );
        }

        $html .= '</li>';
    }

    $html .= sprintf('</%s>', esc_attr($tag));

    return $html;
}
