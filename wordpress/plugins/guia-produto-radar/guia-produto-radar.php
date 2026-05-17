<?php
/**
 * Plugin Name: Guia Produto Radar
 * Plugin URI: https://www.guiaproduto.com.br
 * Description: Exibe dados do Guia Produto Radar no WordPress usando uma API externa leve e cacheada.
 * Version: 0.1.1
 * Author: Guia Produto
 * Text Domain: guia-produto-radar
 * Requires at least: 6.0
 * Requires PHP: 7.4
 */

if (!defined('ABSPATH')) {
    exit;
}

define('GPR_VERSION', '0.1.1');
define('GPR_PLUGIN_FILE', __FILE__);
define('GPR_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('GPR_PLUGIN_URL', plugin_dir_url(__FILE__));
define('GPR_OPTION_ENVIRONMENT', 'gpr_environment');
define('GPR_OPTION_API_BASE_URL', 'gpr_api_base_url');
define('GPR_OPTION_CACHE_TTL', 'gpr_cache_ttl');
define('GPR_OPTION_DEBUG_MODE', 'gpr_debug_mode');
define('GPR_DEFAULT_ENVIRONMENT', 'local');
define('GPR_DEFAULT_API_BASE_URL', 'http://localhost:18080');
define('GPR_DEFAULT_CACHE_TTL', 5 * MINUTE_IN_SECONDS);
define('GPR_MIN_CACHE_TTL', MINUTE_IN_SECONDS);
define('GPR_MAX_CACHE_TTL', DAY_IN_SECONDS);

require_once GPR_PLUGIN_DIR . 'includes/api-client.php';
require_once GPR_PLUGIN_DIR . 'includes/admin.php';
require_once GPR_PLUGIN_DIR . 'includes/shortcodes.php';

function gpr_activate_plugin(): void
{
    if (false === get_option(GPR_OPTION_ENVIRONMENT)) {
        add_option(GPR_OPTION_ENVIRONMENT, GPR_DEFAULT_ENVIRONMENT);
    }

    if (false === get_option(GPR_OPTION_API_BASE_URL)) {
        add_option(GPR_OPTION_API_BASE_URL, GPR_DEFAULT_API_BASE_URL);
    }

    if (false === get_option(GPR_OPTION_CACHE_TTL)) {
        add_option(GPR_OPTION_CACHE_TTL, GPR_DEFAULT_CACHE_TTL);
    }

    if (false === get_option(GPR_OPTION_DEBUG_MODE)) {
        add_option(GPR_OPTION_DEBUG_MODE, '0');
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
