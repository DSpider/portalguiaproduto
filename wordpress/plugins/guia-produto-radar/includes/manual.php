<?php

if (!defined('ABSPATH')) {
    exit;
}

function gpr_render_manual_page(): void
{
    if (!current_user_can('manage_options')) {
        wp_die(esc_html__('Voce nao tem permissao para acessar esta pagina.', 'guia-produto-radar'));
    }

    ?>
    <div class="wrap">
        <h1><?php echo esc_html__('Manual Guia Produto Radar', 'guia-produto-radar'); ?></h1>
        <p>
            <?php echo esc_html__('Este manual explica o objetivo do plugin, como usar os shortcodes e como manter a integracao com a API do Radar sem quebrar o WordPress.', 'guia-produto-radar'); ?>
        </p>

        <h2 class="nav-tab-wrapper">
            <a class="nav-tab nav-tab-active" href="#manual-usuario"><?php echo esc_html__('Manual do usuario', 'guia-produto-radar'); ?></a>
            <a class="nav-tab" href="#manual-tecnico"><?php echo esc_html__('Manual tecnico', 'guia-produto-radar'); ?></a>
            <a class="nav-tab" href="#reversao"><?php echo esc_html__('Reversao', 'guia-produto-radar'); ?></a>
        </h2>

        <section id="manual-usuario">
            <h2><?php echo esc_html__('1. Manual do usuario', 'guia-produto-radar'); ?></h2>

            <h3><?php echo esc_html__('Objetivo principal', 'guia-produto-radar'); ?></h3>
            <p>
                <?php echo esc_html__('O Guia Produto Radar conecta o WordPress do Guia Produto a uma API externa responsavel por tendencias, rankings, scores e dados de produtos. O WordPress continua sendo a vitrine publica; a inteligencia pesada fica fora do WordPress.', 'guia-produto-radar'); ?>
            </p>

            <h3><?php echo esc_html__('O que o plugin faz', 'guia-produto-radar'); ?></h3>
            <ul>
                <li><?php echo esc_html__('Busca dados da API do Guia Produto Radar.', 'guia-produto-radar'); ?></li>
                <li><?php echo esc_html__('Exibe blocos por shortcode em paginas ou posts.', 'guia-produto-radar'); ?></li>
                <li><?php echo esc_html__('Usa cache com transients para evitar excesso de chamadas.', 'guia-produto-radar'); ?></li>
                <li><?php echo esc_html__('Mostra mensagem amigavel se a API estiver offline.', 'guia-produto-radar'); ?></li>
                <li><?php echo esc_html__('Carrega CSS somente nas paginas que usam shortcodes do Radar.', 'guia-produto-radar'); ?></li>
                <li><?php echo esc_html__('Nao publica posts, nao altera tema e nao depende do Elementor.', 'guia-produto-radar'); ?></li>
            </ul>

            <h3><?php echo esc_html__('Configuracoes', 'guia-produto-radar'); ?></h3>
            <table class="widefat striped">
                <tbody>
                    <tr>
                        <th scope="row"><?php echo esc_html__('Ambiente', 'guia-produto-radar'); ?></th>
                        <td><?php echo esc_html__('Use local para desenvolvimento, staging para testes na VPS e producao somente quando tudo estiver aprovado.', 'guia-produto-radar'); ?></td>
                    </tr>
                    <tr>
                        <th scope="row"><?php echo esc_html__('URL base da API', 'guia-produto-radar'); ?></th>
                        <td><?php echo esc_html__('Endereco que o WordPress usa para consultar a API. Na mesma VPS, prefira http://127.0.0.1:28080 em staging.', 'guia-produto-radar'); ?></td>
                    </tr>
                    <tr>
                        <th scope="row"><?php echo esc_html__('Tempo de cache', 'guia-produto-radar'); ?></th>
                        <td><?php echo esc_html__('Tempo, em segundos, que o WordPress guarda a resposta da API. Recomendado: 300 segundos.', 'guia-produto-radar'); ?></td>
                    </tr>
                    <tr>
                        <th scope="row"><?php echo esc_html__('Modo debug', 'guia-produto-radar'); ?></th>
                        <td><?php echo esc_html__('Use apenas durante diagnostico. Ele registra erros no log se WP_DEBUG estiver ativo, mas nao mostra detalhes ao visitante.', 'guia-produto-radar'); ?></td>
                    </tr>
                </tbody>
            </table>

            <h3><?php echo esc_html__('Shortcodes disponiveis', 'guia-produto-radar'); ?></h3>
            <table class="widefat striped">
                <thead>
                    <tr>
                        <th><?php echo esc_html__('Shortcode', 'guia-produto-radar'); ?></th>
                        <th><?php echo esc_html__('Uso', 'guia-produto-radar'); ?></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><code>[guia_produto_radar]</code></td>
                        <td><?php echo esc_html__('Mostra um resumo do Radar com produtos destacados.', 'guia-produto-radar'); ?></td>
                    </tr>
                    <tr>
                        <td><code>[guia_produto_ranking categoria="tecnologia" limite="10"]</code></td>
                        <td><?php echo esc_html__('Mostra um ranking filtrado por categoria e limite.', 'guia-produto-radar'); ?></td>
                    </tr>
                    <tr>
                        <td><code>[guia_produto_tendencias limite="10"]</code></td>
                        <td><?php echo esc_html__('Mostra produtos em tendencia conforme o resumo da API.', 'guia-produto-radar'); ?></td>
                    </tr>
                </tbody>
            </table>

            <h3><?php echo esc_html__('Pagina de teste recomendada', 'guia-produto-radar'); ?></h3>
            <p><?php echo esc_html__('Crie uma pagina manual chamada Radar Teste, com slug radar-teste, e adicione o shortcode abaixo:', 'guia-produto-radar'); ?></p>
            <p><code>[guia_produto_radar]</code></p>
            <p><?php echo esc_html__('O plugin adiciona noindex,nofollow automaticamente para a pagina com slug radar-teste.', 'guia-produto-radar'); ?></p>
        </section>

        <hr>

        <section id="manual-tecnico">
            <h2><?php echo esc_html__('2. Manual tecnico e manutencao', 'guia-produto-radar'); ?></h2>

            <h3><?php echo esc_html__('Arquitetura resumida', 'guia-produto-radar'); ?></h3>
            <p><?php echo esc_html__('WordPress renderiza o site publico. O plugin consulta a API. A API conversa com PostgreSQL e Redis. O worker executa tarefas em background. O admin do Radar roda separado do WordPress.', 'guia-produto-radar'); ?></p>

            <h3><?php echo esc_html__('Caminhos importantes na VPS', 'guia-produto-radar'); ?></h3>
            <ul>
                <li><code>/home/guiaproduto/htdocs/www.guiaproduto.com.br</code> - <?php echo esc_html__('WordPress publico.', 'guia-produto-radar'); ?></li>
                <li><code>/home/guiaproduto/htdocs/www.guiaproduto.com.br/wp-content/plugins/guia-produto-radar</code> - <?php echo esc_html__('plugin instalado no WordPress.', 'guia-produto-radar'); ?></li>
                <li><code>/opt/guia-produto-radar</code> - <?php echo esc_html__('repositorio do Radar na VPS.', 'guia-produto-radar'); ?></li>
                <li><code>/var/backups/guia-produto-radar</code> - <?php echo esc_html__('backups sugeridos do Radar.', 'guia-produto-radar'); ?></li>
            </ul>

            <h3><?php echo esc_html__('Enderecos e portas', 'guia-produto-radar'); ?></h3>
            <table class="widefat striped">
                <thead>
                    <tr>
                        <th><?php echo esc_html__('Ambiente', 'guia-produto-radar'); ?></th>
                        <th><?php echo esc_html__('Uso recomendado', 'guia-produto-radar'); ?></th>
                        <th><?php echo esc_html__('Observacao', 'guia-produto-radar'); ?></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><?php echo esc_html__('Local Windows', 'guia-produto-radar'); ?></td>
                        <td><code>http://localhost:18080</code></td>
                        <td><?php echo esc_html__('Usado durante desenvolvimento local.', 'guia-produto-radar'); ?></td>
                    </tr>
                    <tr>
                        <td><?php echo esc_html__('Staging na VPS', 'guia-produto-radar'); ?></td>
                        <td><code>http://127.0.0.1:28080</code></td>
                        <td><?php echo esc_html__('Recomendado para o WordPress consumir a API sem passar pela internet.', 'guia-produto-radar'); ?></td>
                    </tr>
                    <tr>
                        <td><?php echo esc_html__('Admin staging no navegador', 'guia-produto-radar'); ?></td>
                        <td><code>https://radar-staging.guiaproduto.com.br</code></td>
                        <td><?php echo esc_html__('Acesso protegido por senha ou Cloudflare Access.', 'guia-produto-radar'); ?></td>
                    </tr>
                    <tr>
                        <td><?php echo esc_html__('Producao futura', 'guia-produto-radar'); ?></td>
                        <td><code>http://127.0.0.1:38080</code></td>
                        <td><?php echo esc_html__('Porta sugerida para separar producao de staging.', 'guia-produto-radar'); ?></td>
                    </tr>
                </tbody>
            </table>

            <h3><?php echo esc_html__('Opcoes salvas pelo plugin', 'guia-produto-radar'); ?></h3>
            <ul>
                <li><code>gpr_environment</code> - <?php echo esc_html__('ambiente selecionado.', 'guia-produto-radar'); ?></li>
                <li><code>gpr_api_base_url</code> - <?php echo esc_html__('URL base da API.', 'guia-produto-radar'); ?></li>
                <li><code>gpr_cache_ttl</code> - <?php echo esc_html__('tempo de cache em segundos.', 'guia-produto-radar'); ?></li>
                <li><code>gpr_debug_mode</code> - <?php echo esc_html__('modo debug.', 'guia-produto-radar'); ?></li>
            </ul>

            <h3><?php echo esc_html__('Comandos uteis na VPS', 'guia-produto-radar'); ?></h3>
            <pre><code>cd /opt/guia-produto-radar
docker compose --env-file .env.staging -f docker-compose.staging.yml ps
curl http://127.0.0.1:28080/health
docker compose --env-file .env.staging -f docker-compose.staging.yml logs -f api</code></pre>

            <h3><?php echo esc_html__('Atualizacao manual do plugin', 'guia-produto-radar'); ?></h3>
            <pre><code>WP_PATH=/home/guiaproduto/htdocs/www.guiaproduto.com.br
PLUGIN_SRC=/opt/guia-produto-radar/wordpress/plugins/guia-produto-radar
PLUGIN_DST=$WP_PATH/wp-content/plugins/guia-produto-radar

rm -rf "$PLUGIN_DST"
cp -a "$PLUGIN_SRC" "$PLUGIN_DST"
chown -R guiaproduto:guiaproduto "$PLUGIN_DST"
find "$PLUGIN_DST" -type d -exec chmod 755 {} \;
find "$PLUGIN_DST" -type f -exec chmod 644 {} \;</code></pre>

            <h3><?php echo esc_html__('Seguranca', 'guia-produto-radar'); ?></h3>
            <ul>
                <li><?php echo esc_html__('Nao salve tokens ou senhas na URL da API.', 'guia-produto-radar'); ?></li>
                <li><?php echo esc_html__('Nao exponha PostgreSQL ou Redis na internet.', 'guia-produto-radar'); ?></li>
                <li><?php echo esc_html__('Mantenha o admin do Radar protegido por senha.', 'guia-produto-radar'); ?></li>
                <li><?php echo esc_html__('Mantenha o modo debug desligado no uso normal.', 'guia-produto-radar'); ?></li>
                <li><?php echo esc_html__('Faca backup antes de atualizar plugin ou containers.', 'guia-produto-radar'); ?></li>
            </ul>
        </section>

        <hr>

        <section id="reversao">
            <h2><?php echo esc_html__('3. Reversao rapida', 'guia-produto-radar'); ?></h2>
            <p><?php echo esc_html__('Se algo der errado, desative o plugin. O WordPress deve continuar funcionando sem os blocos do Radar.', 'guia-produto-radar'); ?></p>
            <pre><code>WP_PATH=/home/guiaproduto/htdocs/www.guiaproduto.com.br
sudo -u guiaproduto wp --path="$WP_PATH" plugin deactivate guia-produto-radar</code></pre>
            <p><?php echo esc_html__('Tambem e possivel desativar pelo painel em Plugins > Guia Produto Radar > Desativar.', 'guia-produto-radar'); ?></p>
        </section>
    </div>
    <?php
}
