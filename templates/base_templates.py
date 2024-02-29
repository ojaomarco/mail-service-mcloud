HTML_TEMPLATE2 = """

<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mcloud</title>
<style>
    body {{
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f4f4f4;
    }}
    .container {{
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px;
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    h1 {{
        color: #333333;
    }}
    p {{
        color: #666666;
    }}
    .footer {{
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid #dddddd;
        text-align: center;
        color: #999999;
    }}
</style>
</head>
<body>

<div class="container">
    <img src="https://i.upimg.com/0eg6EfQoR" width="200px"></img>
    <!-- <h1>MCloud</h1> -->
    <p>Olá, {user_name},</p>
    <p>Este é um email automático para informar que a sua sopradora possui o sistema de monitoramento remoto Mcloud, porém encontra-se <b>{status_maquina}</b>.</p>
    
    <p>Por favor, entre em contato com o suporte da Multipet para ATIVAR o seu dispositivo</p>

    <p>Com o sistema em funcionamento, é possivel </p>

    <p>Atenciosamente,</p>
    <p>Equipe Multipet</p>
</div>

<div class="footer">
    <p>&copy; 2024 Multipet Sopradoras</p>
</div>

</body>
</html>
"""


HTML_TEMPLATE = """
   <html lang="pt-br" style="margin: 0;padding: 0;box-sizing: border-box;">

<head style="margin: 0;padding: 0;box-sizing: border-box;">
   <style>
.im {{
    color: inherit !important;
  }}
  div > span.im {{
    color: inherit !important;
  }}
  p > span.im {{
    color: inherit !important;
  }}</style>
    <meta charset="utf-8">
    <title>MCloud</title>
    <meta name="author" content="MCloud">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">    

    <script style="margin: 0;padding: 0;box-sizing: border-box;">
        $(window).on("load resize ", function () {{
            var scrollWidth = $('.tbl-content').width() - $('.tbl-content table').width();
            $('.tbl-header').css({{ 'padding-right': scrollWidth }});
        }}).resize();
    </script>
</head>

<body style="margin: 0;padding: 0;box-sizing: border-box;font-weight: 300;font-family: system-ui;background-color: #0a1f3c;color: white;">
    <div class="container" style="margin: 0 auto;padding: 0;box-sizing: border-box;max-width: 800px;">
        <div class="section" style="margin: 0;padding: 20px;box-sizing: border-box;background-color: #1c3b5f;">
            <img src="https://i.upimg.com/0eg6EfQoR" width="200px" style="margin: 0;padding: 0;box-sizing: border-box;">
            <div class="section-title" style="margin: 0;padding: 0;box-sizing: border-box;margin-top: 15px;font-size: 24px;font-weight: 500;">Olá, {user_name}.</div>
            <div class="summary" style="margin: 0;padding: 0;box-sizing: border-box;font-size: 18px;margin-top: 10px;">Este é um email automático para informar sobre o status do seu equipamento Multipet com
                o número de série {serial_number}.</div>

            <div class="section-content " style="margin: 0;padding: 0;box-sizing: border-box;font-size: 20px;margin-top: 10px;">

                <div class="comparison " style="margin: 0;padding: 0;box-sizing: border-box;">Dados referentes as últimas 24 horas.</div>

            </div>
            <div class="section-card" style="margin: 0;padding: 0;box-sizing: border-box;display: flex;align-items: baseline;justify-content: center;">
                <div class="card" style="margin: 2px;padding: 5px;box-sizing: border-box;width: 50%;background-color: #3f5b81;border-radius: 2%;">
                    <div class="big-number" style="margin: 0;padding: 0;box-sizing: border-box;text-align: center;font-size: 72px;font-weight: 500;">{total_prod}</div>
                    <div class="text-card" style="margin: 0;padding: 0;box-sizing: border-box;font-size: 16px;text-align: center;">Total de Garrafas Produzidas</div>
                </div>
                <div class="card" style="margin: 2px;padding: 5px;box-sizing: border-box;width: 50%;background-color: #3f5b81;border-radius: 2%;">
                    <div class="big-number" style="margin: 0;padding: 0;box-sizing: border-box;text-align: center;font-size: 72px;font-weight: 500;">{prod_hora}</div>
                    <div class="text-card" style="margin: 0;padding: 0;box-sizing: border-box;font-size: 16px;text-align: center;">Velocidade Média de Produção (G/h)</div>
                </div>
            </div>
            <div class="section-card" style="margin: 0;padding: 0;box-sizing: border-box;display: flex;align-items: baseline;justify-content: center;">
                <div class="card" style="margin: 2px;padding: 5px;box-sizing: border-box;width: 50%;background-color: #3f5b81;border-radius: 2%;">
                    <div class="big-number" style="margin: 0;padding: 0;box-sizing: border-box;text-align: center;font-size: 72px;font-weight: 500;">{press_baixa}</div> 
                    <div class="text-card" style="margin: 0;padding: 0;box-sizing: border-box;font-size: 16px;text-align: center;">Pressão Média Ar de Baixa (Bar)</div>
                </div>
                <div class="card" style="margin: 2px;padding: 5px;box-sizing: border-box;width: 50%;background-color: #3f5b81;border-radius: 2%;">
                    <div class="big-number" style="margin: 0;padding: 0;box-sizing: border-box;text-align: center;font-size: 72px;font-weight: 500;">{press_alta}</div>
                    <div class="text-card" style="margin: 0;padding: 0;box-sizing: border-box;font-size: 16px;text-align: center;">Pressão Média Ar de Alta (Bar)</div>
                </div>
            </div>
            <div class="section-card" style="margin: 0;padding: 0;box-sizing: border-box;display: flex;align-items: baseline;justify-content: center;">
                <div class="card" style="margin: 2px;padding: 5px;box-sizing: border-box;width: 50%;background-color: #3f5b81;border-radius: 2%;">
                    <div class="big-number" style="margin: 0;padding: 0;box-sizing: border-box;text-align: center;font-size: 72px;font-weight: 500;"> {temp_coifa} </div>
                    <div class="text-card" style="margin: 0;padding: 0;box-sizing: border-box;font-size: 16px;text-align: center;">Temperatura Média Coifa (ºC)</div>
                </div>
            </div>
        </div>
        <div class="section " style="margin: 0;padding: 20px;box-sizing: border-box;background-color: #1c3b5f;">

            <div class="section-content section-card section-title" style="margin: 0;padding: 0;box-sizing: border-box;display: flex;align-items: baseline;justify-content: center;margin-top: 10px;font-size: 20px;font-weight: 500;">Tabela de Falhas</div>
            <br style="margin: 0;padding: 0;box-sizing: border-box;">
            <div align="center" style="margin: 0;padding: 0;box-sizing: border-box;">
                <div class="tbl-header" style="margin: 0;padding: 0;box-sizing: border-box;">
                    <table cellpadding="0" cellspacing="0" border="0" style="margin: 0;padding: 0;box-sizing: border-box;width: 80%;table-layout: auto;">
                        <thead style="margin: 0;padding: 0;box-sizing: border-box;background-color: rgba(255, 255, 255, 0.3);">
                            <tr style="margin: 0;padding: 0;box-sizing: border-box;">
                                <th style="margin: 0;padding: 10px 5px;box-sizing: border-box;text-align: left;font-weight: 500;font-size: 15px;color: #fff;text-transform: uppercase;">Hora</th>
                                <th style="margin: 0;padding: 10px 5px;box-sizing: border-box;text-align: left;font-weight: 500;font-size: 15px;color: #fff;text-transform: uppercase;">Descrição</th>
                            </tr>
                        </thead>
                    </table>
                </div>
                <div class="tbl-content" style="margin: 0;padding: 0;box-sizing: border-box;height: 300px;overflow-x: auto;">
                    {issues_table}
                </div>

            </div>
        </div>

</div></body>
</html>


"""
