<?php

if (!defined('ABSPATH')) {
    exit;
}

function gpr_register_admin_hooks(): void
{
    add_action('admin_menu', 'gpr_register_admin_page');
    add_action('admin_init', 'gpr_register_settings');
}

function gpr_register_admin_page(): void
{
    add_options_page(
        'Guia Produto Radar',
        'Guia Produto Radar',
        'manage_options',
        'guia-produto-radar',
        'gpr_render_admin_page'
    );

    add_options_page(
        'Manual Guia Produto Radar',
        'Manual Guia Produto Radar',
        'manage_options',
        'guia-produto-radar-manual',
        'gpr_render_manual_page'
    );
}

function gpr_register_settings(): void
{
    register_setting(
        'gpr_settings',
        GPR_OPTION_ENVIRONMENT,
        array(
            'type' => 'string',
            'sanitize_callback' => 'gpr_sanitize_environment',
            'default' => GPR_DEFAULT_ENVIRONMENT,
        )
    );

    register_setting(
        'gpr_settings',
        GPR_OPTION_API_BASE_URL,
        array(
            'type' => 'string',
            'sanitize_callback' => 'gpr_sanitize_api_base_url',
            'default' => GPR_DEFAULT_API_BASE_URL,
        )
    );

    register_setting(
        'gpr_settings',
        GPR_OPTION_CACHE_TTL,
        array(
            'type' => 'integer',
            'sanitize_callback' => 'gpr_sanitize_cache_ttl',
            'default' => GPR_DEFAULT_CACHE_TTL,
        )
    );

    register_setting(
        'gpr_settings',
        GPR_OPTION_DEBUG_MODE,
        array(
            'type' => 'string',
            'sanitize_callback' => 'gpr_sanitize_debug_mode',
            'default' => '0',
        )
    );

    add_settings_section(
        'gpr_api_section',
        'API do Guia Produto Radar',
        'gpr_render_api_section',
        'guia-produto-radar'
    );

    add_settings_field(
        GPR_OPTION_ENVIRONMENT,
        'Ambiente',
        'gpr_render_environment_field',
        'guia-produto-radar',
        'gpr_api_section'
    );

    add_settings_field(
        GPR_OPTION_API_BASE_URL,
        'URL base da API',
        'gpr_render_api_base_url_field',
        'guia-produto-radar',
        'gpr_api_section'
    );

    add_settings_field(
        GPR_OPTION_CACHE_TTL,
        'Tempo de cache',
        'gpr_render_cache_ttl_field',
        'guia-produto-radar',
        'gpr_api_section'
    );

    add_settings_field(
        GPR_OPTION_DEBUG_MODE,
        'Modo debug',
        'gpr_render_debug_mode_field',
        'guia-produto-radar',
        'gpr_api_section'
    );
}

function gpr_render_api_section(): void
{
    echo '<p>Configure a API do Radar com valores seguros. Em producao na mesma VPS, prefira <code>http://127.0.0.1:28080</code>.</p>';
}

function gpr_render_environment_field(): void
{
    $value = gpr_get_environment();
    $options = array(
        'local' => 'Local',
        'staging' => 'Staging',
        'production' => 'Producao',
    );

    echo '<select id="' . esc_attr(GPR_OPTION_ENVIRONMENT) . '" name="' . esc_attr(GPR_OPTION_ENVIRONMENT) . '">';
    foreach ($options as $option_value => $label) {
        printf(
            '<option value="%1$s" %2$s>%3$s</option>',
            esc_attr($option_value),
            selected($value, $option_value, false),
            esc_html($label)
        );
    }
    echo '</select>';
    echo '<p class="description">Use staging para testar no WordPress real antes de qualquer uso amplo.</p>';
}

function gpr_render_api_base_url_field(): void
{
    $value = gpr_get_api_base_url();

    printf(
        '<input type="url" class="regular-text code" id="%1$s" name="%1$s" value="%2$s" placeholder="http://localhost:18080" />',
        esc_attr(GPR_OPTION_API_BASE_URL),
        esc_attr($value)
    );
    echo '<p class="description">Nao informe tokens ou credenciais neste campo.</p>';
}

function gpr_render_cache_ttl_field(): void
{
    $value = gpr_get_cache_ttl();

    printf(
        '<input type="number" min="%1$d" max="%2$d" step="60" class="small-text" id="%3$s" name="%3$s" value="%4$d" /> segundos',
        esc_attr(GPR_MIN_CACHE_TTL),
        esc_attr(GPR_MAX_CACHE_TTL),
        esc_attr(GPR_OPTION_CACHE_TTL),
        esc_attr($value)
    );
    echo '<p class="description">Minimo de 60 segundos e maximo de 86400 segundos. Valor recomendado: 300.</p>';
}

function gpr_render_debug_mode_field(): void
{
    $enabled = gpr_is_debug_mode();

    printf(
        '<label><input type="checkbox" id="%1$s" name="%1$s" value="1" %2$s /> Registrar erros da API no log quando <code>WP_DEBUG</code> estiver ativo.</label>',
        esc_attr(GPR_OPTION_DEBUG_MODE),
        checked($enabled, true, false)
    );
    echo '<p class="description">Nao exibe erros tecnicos para visitantes. Use apenas durante testes.</p>';
}

function gpr_render_admin_page(): void
{
    if (!current_user_can('manage_options')) {
        wp_die(esc_html__('Voce nao tem permissao para acessar esta pagina.', 'guia-produto-radar'));
    }

    ?>
    <div class="wrap">
        <h1><?php echo esc_html__('Guia Produto Radar', 'guia-produto-radar'); ?></h1>
        <p>
            <a class="button button-secondary" href="<?php echo esc_url(admin_url('options-general.php?page=guia-produto-radar-manual')); ?>">
                <?php echo esc_html__('Abrir manual completo do plugin', 'guia-produto-radar'); ?>
            </a>
        </p>
        <form method="post" action="options.php">
            <?php
            settings_fields('gpr_settings');
            do_settings_sections('guia-produto-radar');
            submit_button('Salvar configuracao');
            ?>
        </form>
    </div>
    <?php
}
