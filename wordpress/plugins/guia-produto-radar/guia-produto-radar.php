<?php
/**
 * Plugin Name: Guia Produto Radar
 * Plugin URI: https://www.guiaproduto.com.br
 * Description: Exibe dados do Guia Produto Radar no WordPress usando uma API externa leve e cacheada.
 * Version: 0.1.0
 * Author: Guia Produto
 * Text Domain: guia-produto-radar
 * Requires at least: 6.0
 * Requires PHP: 7.4
 */

if (!defined('ABSPATH')) {
    exit;
}

define('GPR_VERSION', '0.1.0');
define('GPR_PLUGIN_FILE', __FILE__);
define('GPR_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('GPR_PLUGIN_URL', plugin_dir_url(__FILE__));
define('GPR_OPTION_API_BASE_URL', 'gpr_api_base_url');
define('GPR_DEFAULT_API_BASE_URL', 'http://localhost:18080');
define('GPR_CACHE_TTL', 5 * MINUTE_IN_SECONDS);

require_once GPR_PLUGIN_DIR . 'includes/api-client.php';
require_once GPR_PLUGIN_DIR . 'includes/admin.php';
require_once GPR_PLUGIN_DIR . 'includes/shortcodes.php';

function gpr_activate_plugin(): void
{
    if (false === get_option(GPR_OPTION_API_BASE_URL)) {
        add_option(GPR_OPTION_API_BASE_URL, GPR_DEFAULT_API_BASE_URL);
    }
}
register_activation_hook(__FILE__, 'gpr_activate_plugin');

function gpr_bootstrap_plugin(): void
{
    gpr_register_shortcodes();

    if (is_admin()) {
        gpr_register_admin_hooks();
    }
}
add_action('plugins_loaded', 'gpr_bootstrap_plugin');
