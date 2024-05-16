HTML_TEMPLATE_ERRO = """
<!DOCTYPE html>
<html lang="pt-br">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Status do Equipamento Multipet</title>
    
</head>

<body style="margin: 0;padding: 0;font-family: Georgi, sans-serif;background-color: #f2f2f2;color: #333;">
    <div class="container" style="max-width: 800px;margin: 20px auto;padding: 20px;background-color: #fff;border-radius: 5px;box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
        <div class="header" style="text-align: center;margin-bottom: 20px;">
            <img src="https://i.upimg.com/0eg6EfQoR" alt="Logo" class="logo" style="max-width: 200px;margin-bottom: 20px;">
            <h1>Status do Equipamento Multipet</h1>
        </div>
        <div class="section">
            <h2 class="section-title" style="font-size: 24px;font-weight: bold;margin-bottom: 10px;">Olá, {user_name}.</h2>
            <p class="summary" style="font-size: 18px;margin-bottom: 10px;">Este é um email automático para informar que seu equipamento Multipet com o número de série <strong>{serial_number}</strong>, possui o sistema MCloud de monitoramento remoto, porém encontra-se desativado.</p>
            <p class="summary" style="font-size: 18px;margin-bottom: 10px;">Por favor, entre em contato com o suporte da Multipet para <strong>ATIVAR</strong> o seu dispositivo</p>
            <p class="summary" style="font-size: 18px;margin-bottom: 10px;">Com o sistema em funcionamento, é possivel monitorar o desempenho de sua máquina remotamente e também receber informações diariamente sobre a produção.</p>
            <p class="summary" style="font-size: 18px;margin-bottom: 10px;">Atenciosamente,<br>Equipe Multipet</p>
        </div>
    </div>
        
    
</div></body>

</html>

"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-br" style="margin: 0;padding: 0;box-sizing: border-box;">

<head style="margin: 0;padding: 0;box-sizing: border-box;">
   <style>
    .table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}

        .table th,
        .table td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }}

        .table th {{
            background-color: #f2f2f2;
            font-weight: bold;
            text-transform: uppercase;
            color: #666;
        }}
   
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

<body style="margin: 0;padding: 0;font-family: Arial, sans-serif;background-color: #f2f2f2;color: #333;">
    <div class="container" style="max-width: 800px;margin: 20px auto;padding: 20px;background-color: #fff;border-radius: 5px;box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
        <div class="header" style="text-align: center;margin-bottom: 20px;">
            <img src="https://i.upimg.com/0eg6EfQoR" alt="Logo" class="logo" style="max-width: 200px;margin-bottom: 20px;">
            <h1>Status do Equipamento Multipet</h1>
        </div>
        <div class="section">
            <h2 class="section-title" style="font-size: 24px;font-weight: bold;margin-bottom: 10px;">Olá, {user_name}.</h2>
            <p class="summary" style="font-size: 18px;margin-bottom: 10px;">Este é um email automático para informar sobre o status do seu equipamento Multipet com o número de série <strong>{serial_number}.</strong></p>
            <p class="summary" style="font-size: 18px;margin-bottom: 10px;">Tempo de sopradora ligada nas últimas 24 horas: <strong>{running_time}</strong></p>
            <p class="summary" style="font-size: 18px;margin-bottom: 10px;">Tempo de sopradora alimentando e produzindo nas últimas 24 horas: <strong>{horas_alimentando}</strong></p>
            <div class="section-card" style="align-items: baseline;display: flex;">           
            <div class="card" style="background-color: #f2f2f2;padding: 20px;border-radius: 5px;margin-bottom: 20px;width: 50%;margin: 2px;">
                <div class="big-number" style="font-size: 48px;font-weight: bold;margin-bottom: 10px;color: #333;">{total_prod}</div>
                <div class="text-card" style="font-size: 16px;color: #666;">Total de Garrafas Produzidas</div>
            </div>
            <div class="card" style="background-color: #f2f2f2;padding: 20px;border-radius: 5px;margin-bottom: 20px;width: 50%;margin: 2px;">
                <div class="big-number" style="font-size: 48px;font-weight: bold;margin-bottom: 10px;color: #333;">{prod_hora}</div>
                <div class="text-card" style="font-size: 16px;color: #666;">Velocidade Média de Produção (G/h)</div>
            </div>
        </div>
    </div>
        <div class="section">
            <div class="graph-container" style="display: flex;justify-content: space-between;margin-bottom: 20px;">
    <div style="background-color: #f2f2f2; padding: 20px; border-radius: 5px;margin-right:2px">
        <img src="cid:image1" alt="Gráfico de Pressão" class="graph" style="max-width: 100%;height: auto;">
        <p style="text-align: center; font-size: 16px;color: #666; ">Gráfico de Pressão</p>
    </div>
    <div style="background-color: #f2f2f2; padding: 20px; border-radius: 5px;margin-left:2px">
        <img src="cid:image2" alt="Gráfico de Eficiência" class="graph" style="max-width: 100%;height: auto;">
        <p style="text-align: center; font-size: 16px; color: #666;">Gráfico de Eficiência</p>
    </div>
</div>
<p><strong>A eficiência do seu equipamento foi calculada com base no tempo total de máquina ligada e na velocidade média. A eficiência é expressa como a porcentagem da produção total em relação à produção esperada durante o mesmo período de tempo.</strong></p>
        </div>
        
            <br style="margin: 0;padding: 0;box-sizing: border-box;">
            <div align="center" style="margin: 0;padding: 0;box-sizing: border-box;">
                
                <div class="tbl-content" style="margin: 0;padding: 0;box-sizing: border-box;height: 300px;overflow-x: auto;">
                <h2 style="text-align: center">Tabela de falhas</h2>
                    {issues_table}
                </div>

            </div>
            <br>
            <p><strong>Informamos que o serviço de emails está atualmente em fase beta e, por isso, pode apresentar algumas falhas e inconsistências nos dados. Agradecemos sua compreensão e paciência enquanto trabalhamos para aprimorar o sistema.</strong></p>
            <p><strong>Atenciosamente, <br>Equipe Multipet</strong></p>
        </div>
    </div>
</body>

</html>
"""

HTML_TEMPLATE3 = """
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

            <div class="summary" style="margin: 0;padding: 0;box-sizing: border-box;font-size: 18px;margin-top: 10px;">Tempo de sopradora ligada nas ultimas 24 horas: {running_time}</div> 
            <div class="summary" style="margin: 0;padding: 0;box-sizing: border-box;font-size: 18px;margin-top: 10px;">Tempo de sopradora alimentando e produzindo nas ultimas 24 horas: {horas_alimentando}</div>       
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
            
            <div class="section-card" style="margin: 0;padding: 0;box-sizing: border-box; margin:2px;display: flex;align-items: baseline;justify-content: center;">
                <div class="card" style="margin: 2px;padding: 5px;box-sizing: border-box;width: 100%;background-color: #ffffff;border-radius: 2%;">
                    <div class="big-number" style="margin: 0;padding: 0;box-sizing: border-box;text-align: center;font-size: 72px;font-weight: 500;">  <img src="cid:image1" alt="Gráfico de Pressão" width="500px"> </div>
                    
                </div>
                <div class="card" style="margin: 2px;padding: 5px;box-sizing: border-box;width: 100%;background-color: #ffffff;border-radius: 2%;">
                    <div class="big-number" style="margin: 0;padding: 0;box-sizing: border-box;text-align: center;font-size: 72px;font-weight: 500;">  <img src="cid:image2" alt="Gráfico de Eficiencia" width="400px"> </div>
                    
                </div>
            </div>
        </div>
       
        <div class="section " style="margin: 0;padding: 20px;box-sizing: border-box;background-color: #1c3b5f;">
            <br style="margin: 0;padding: 0;box-sizing: border-box;">
            <div align="center" style="margin: 0;padding: 0;box-sizing: border-box;">
                <div class="tbl-header" style="margin: 0;padding: 0;box-sizing: border-box;">
                    <table cellpadding="0" cellspacing="0" border="0" style="margin: 0;padding: 0;box-sizing: border-box;width: 80%;table-layout: auto;">
                        <thead style="margin: 0;padding: 0;box-sizing: border-box;background-color: rgba(255, 255, 255, 0.3);">
                            <tr style="margin: 0;padding: 0;box-sizing: border-box;">
                                <th style="margin: 0;padding: 7px 5px;box-sizing: border-box;text-align: left;font-weight: 500;font-size: 12px;color: #fff;text-transform: uppercase; width: 100px">Hora Início</th>
                                <th style="margin: 0;padding: 7px 5px;box-sizing: border-box;text-align: left;font-weight: 500;font-size: 12px;color: #fff;text-transform: uppercase; width:150px">Hora Fim</th>
                                <th style="margin: 0;padding: 7px 5px;box-sizing: border-box;text-align: left;font-weight: 500;font-size: 12px;color: #fff;text-transform: uppercase;">Descrição</th>
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
