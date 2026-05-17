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
}

function gpr_register_settings(): void
{
    register_setting(
        'gpr_settings',
        GPR_OPTION_API_BASE_URL,
        array(
            'type' => 'string',
            'sanitize_callback' => 'gpr_sanitize_api_base_url',
            'default' => GPR_DEFAULT_API_BASE_URL,
        )
    );

    add_settings_section(
        'gpr_api_section',
        'API do Guia Produto Radar',
        'gpr_render_api_section',
        'guia-produto-radar'
    );

    add_settings_field(
        GPR_OPTION_API_BASE_URL,
        'URL base da API',
        'gpr_render_api_base_url_field',
        'guia-produto-radar',
        'gpr_api_section'
    );
}

function gpr_render_api_section(): void
{
    echo '<p>Informe a URL base da API. Em desenvolvimento local, use normalmente <code>http://localhost:18080</code>.</p>';
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

function gpr_render_admin_page(): void
{
    if (!current_user_can('manage_options')) {
        wp_die(esc_html__('Voce nao tem permissao para acessar esta pagina.', 'guia-produto-radar'));
    }

    ?>
    <div class="wrap">
        <h1><?php echo esc_html__('Guia Produto Radar', 'guia-produto-radar'); ?></h1>
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
