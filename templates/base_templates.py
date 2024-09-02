HTML_TEMPLATE_FINANCEIRO = """
<!DOCTYPE html>
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
    <div class="container"
        style="max-width: 800px;margin: 20px auto;padding: 20px;background-color: #fff;border-radius: 5px;box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
        <div class="header" style="text-align: center;margin-bottom: 20px;">
            <img src="https://i.upimg.com/0eg6EfQoR" alt="Logo" class="logo"
                style="max-width: 200px;margin-bottom: 20px;">
            <h1>Status do Equipamento Multipet (Saúde)</h1>
        </div>
        <div class="section">
            <h2 class="section-title" style="font-size: 24px;font-weight: bold;margin-bottom: 10px;">Olá, {user_name}.
            </h2>
            <p class="summary" style="font-size: 18px;margin-bottom: 10px;">Este é um email automático para informar
                sobre o status do equipamento Multipet com o número de série <strong>{serial_number}</strong> no período de <strong>{start_date}</strong> a <strong>{end_date}</strong>.</p>
            <p class="summary" style="font-size: 18px;margin-bottom: 10px;">Tempo de sopradora ligada nos últimos 30
                dias: <strong>{running_time}</strong></p>
            <p class="summary" style="font-size: 18px;margin-bottom: 10px;">Tempo de sopradora alimentando e produzindo
                nas últimos 30 dias: <strong>{horas_alimentando}</strong></p>
            <p class="summary" style="font-size: 18px;margin-bottom: 10px;">Garrafas além do limite produzidas: <strong>{producao_saude}</strong></p>
            <div class="section-card" style="align-items: baseline;display: flex;">
                <div class="card"
                    style="background-color: #f2f2f2;padding: 20px;border-radius: 5px;margin-bottom: 20px;width: 50%;margin: 2px;">
                    <div class="big-number" style="font-size: 48px;font-weight: bold;margin-bottom: 10px;color: #333;">
                        {total_prod}</div>
                    <div class="text-card" style="font-size: 16px;color: #666;">Total de Garrafas Produzidas</div>
                </div>
                <div class="card"
                    style="background-color: #f2f2f2;padding: 20px;border-radius: 5px;margin-bottom: 20px;width: 50%;margin: 2px;">
                    <div class="big-number" style="font-size: 48px;font-weight: bold;margin-bottom: 10px;color: #333;">
                        {prod_hora}</div>
                    <div class="text-card" style="font-size: 16px;color: #666;">Velocidade Média de Produção (G/h)</div>
                </div>
            </div>
        </div>
    </div>
    </div>
</body>

</html>
"""
