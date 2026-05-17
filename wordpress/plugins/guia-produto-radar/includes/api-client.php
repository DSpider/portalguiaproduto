<?php

if (!defined('ABSPATH')) {
    exit;
}

function gpr_get_api_base_url(): string
{
    $api_base_url = get_option(GPR_OPTION_API_BASE_URL, GPR_DEFAULT_API_BASE_URL);
    $api_base_url = is_string($api_base_url) ? trim($api_base_url) : '';

    if ('' === $api_base_url) {
        return GPR_DEFAULT_API_BASE_URL;
    }

    return untrailingslashit($api_base_url);
}

function gpr_sanitize_api_base_url($value): string
{
    $value = is_string($value) ? trim($value) : '';
    $value = esc_url_raw($value);

    if ('' === $value) {
        return GPR_DEFAULT_API_BASE_URL;
    }

    $scheme = wp_parse_url($value, PHP_URL_SCHEME);
    if (!in_array($scheme, array('http', 'https'), true)) {
        add_settings_error(
            GPR_OPTION_API_BASE_URL,
            'gpr_invalid_api_url',
            'Informe uma URL de API iniciada por http ou https.',
            'error'
        );

        return gpr_get_api_base_url();
    }

    return untrailingslashit($value);
}

function gpr_build_api_url(string $path): string
{
    return gpr_get_api_base_url() . '/' . ltrim($path, '/');
}

function gpr_get_transient_key(string $path): string
{
    return 'gpr_api_' . md5(gpr_get_api_base_url() . '|' . $path);
}

function gpr_fetch_api_json(string $path, int $ttl = GPR_CACHE_TTL)
{
    $transient_key = gpr_get_transient_key($path);
    $cached = get_transient($transient_key);

    if (false !== $cached) {
        return $cached;
    }

    $response = wp_remote_get(
        gpr_build_api_url($path),
        array(
            'timeout' => 5,
            'headers' => array(
                'Accept' => 'application/json',
            ),
        )
    );

    if (is_wp_error($response)) {
        return $response;
    }

    $status_code = wp_remote_retrieve_response_code($response);
    if ($status_code < 200 || $status_code >= 300) {
        return new WP_Error(
            'gpr_api_bad_status',
            'A API do Guia Produto Radar retornou um status inesperado.'
        );
    }

    $body = wp_remote_retrieve_body($response);
    $decoded = json_decode($body, true);

    if (!is_array($decoded)) {
        return new WP_Error(
            'gpr_api_invalid_json',
            'A API do Guia Produto Radar retornou uma resposta invalida.'
        );
    }

    set_transient($transient_key, $decoded, $ttl);

    return $decoded;
}

function gpr_get_radar_summary()
{
    return gpr_fetch_api_json('/api/v1/radar/summary');
}

function gpr_get_products()
{
    return gpr_fetch_api_json('/api/v1/products');
}
