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

function gpr_get_environment(): string
{
    $environment = get_option(GPR_OPTION_ENVIRONMENT, GPR_DEFAULT_ENVIRONMENT);
    $environment = is_string($environment) ? sanitize_key($environment) : GPR_DEFAULT_ENVIRONMENT;

    if (!in_array($environment, array('local', 'staging', 'production'), true)) {
        return GPR_DEFAULT_ENVIRONMENT;
    }

    return $environment;
}

function gpr_sanitize_environment($value): string
{
    $value = is_string($value) ? sanitize_key($value) : GPR_DEFAULT_ENVIRONMENT;

    if (!in_array($value, array('local', 'staging', 'production'), true)) {
        return GPR_DEFAULT_ENVIRONMENT;
    }

    return $value;
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

function gpr_get_cache_ttl(): int
{
    $ttl = absint(get_option(GPR_OPTION_CACHE_TTL, GPR_DEFAULT_CACHE_TTL));

    if ($ttl < GPR_MIN_CACHE_TTL) {
        return GPR_MIN_CACHE_TTL;
    }

    if ($ttl > GPR_MAX_CACHE_TTL) {
        return GPR_MAX_CACHE_TTL;
    }

    return $ttl;
}

function gpr_sanitize_cache_ttl($value): int
{
    $ttl = absint($value);

    if ($ttl < GPR_MIN_CACHE_TTL) {
        return GPR_MIN_CACHE_TTL;
    }

    if ($ttl > GPR_MAX_CACHE_TTL) {
        return GPR_MAX_CACHE_TTL;
    }

    return $ttl;
}

function gpr_is_debug_mode(): bool
{
    return '1' === (string) get_option(GPR_OPTION_DEBUG_MODE, '0');
}

function gpr_sanitize_debug_mode($value): string
{
    return !empty($value) ? '1' : '0';
}

function gpr_debug_log(string $message): void
{
    if (!gpr_is_debug_mode() || !defined('WP_DEBUG') || !WP_DEBUG) {
        return;
    }

    error_log('[Guia Produto Radar] ' . $message);
}

function gpr_build_api_url(string $path): string
{
    return gpr_get_api_base_url() . '/' . ltrim($path, '/');
}

function gpr_get_transient_key(string $path): string
{
    return 'gpr_api_' . md5(gpr_get_environment() . '|' . gpr_get_api_base_url() . '|' . $path);
}

function gpr_fetch_api_json(string $path, ?int $ttl = null)
{
    $ttl = null === $ttl ? gpr_get_cache_ttl() : gpr_sanitize_cache_ttl($ttl);
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
        gpr_debug_log('Falha ao consultar API em ' . $path . ': ' . $response->get_error_message());
        return $response;
    }

    $status_code = wp_remote_retrieve_response_code($response);
    if ($status_code < 200 || $status_code >= 300) {
        gpr_debug_log('Status inesperado da API em ' . $path . ': ' . (string) $status_code);

        return new WP_Error(
            'gpr_api_bad_status',
            'A API do Guia Produto Radar retornou um status inesperado.'
        );
    }

    $body = wp_remote_retrieve_body($response);
    $decoded = json_decode($body, true);

    if (!is_array($decoded)) {
        gpr_debug_log('JSON invalido recebido da API em ' . $path);

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
