import pandas as pd
alert = {
    'Regua_HomePincas'  : 'Alerta: falha nos sensores de regua aberta, os sensores deveriam estar ligados.'     ,
    'Regua_HomeBocais'  : 'Alerta: falha nos sensores dos bocais embaixo, os sensores deveriam estar ligados.'  ,
    'Regu_Posi'         : 'Alerta: colisão da posicionador e régua.'                                            ,
    'Regu_Bocal'        : 'Alerta: Suba os bocais ou abra as pinças da régua'                                   ,
    'Regu_Pren'         : 'Alerta: Abra a prensa ou abra pinças da régua.'                                      ,
    'Regu_Esti'         : 'Alerta: colisão entre Régua e estiramento.'                                          ,
    'Regu_PincaAber'    : 'Alerta: sensor da régua ligado com a pinça fechada.'                                 ,
    'Regu_PincaFech'    : 'Alerta: sensor da régua desligado com a pinça aberta.'                               ,
    'Prensa_HomeBocai'  : 'Alerta: falha nos sensores dos bocais embaixo, os sensores deveriam estar ligados.'  ,
    'Prensa_Fechar'     : 'Alerta: aguarde o movimento da régua ou abra as pinças da régua.'                    ,
    'Prensa_Abrir'      : 'Alerta: pleno acionado, desligue para abrir a prensa.'                               ,
    'Prensa_CargPleno'  : 'Alerta: a prensa deve estar fechada para ligar o pleno.'                             ,
    'Prensa_DescPleno'  : 'Alerta: a prensa deve estar fechada para ligar o pleno.'                             ,
    'Estira_SensorTop'  : 'Alerta: falha na leitura do sensor do estiramento em cima.'                          ,
    'Estira_Descida'    : 'Alerta: aguarde o movimento da régua ou abra as pinças da régua.'                    ,
    'Estira_BocalSubi'  : 'Alerta: falha nos sensores dos bocais, o sensor deveria estar desligado.'            ,
    'Estira_BocalDesc'  : 'Alerta: falha nos sensores dos bocais embaixo, os sensores deveriam estar ligados.'  ,
    'Estira_BocalRegu'  : 'Alerta: Abra as pinças da régua para descer os bocais.'                              ,
    'Forno_PinFornBai'  : 'Alerta: sensor de pino do forno embaixo acionado.'                                   ,
    'Forno_PFTorna'     : 'Alerta: sensor de pré-forma torta acionado.'                                         ,
    'Forno_SegCamb'     : 'Alerta: segurança de colisão do cambotador com o forno.'                             ,
    'Forno_ManSensorC'  : 'Alerta: came acionado com pouca pré-forma na rampa.'                                 ,
    'Forno_Aquecendo'   : 'Alerta: forno Aquecendo.'                                                            ,
    'Mesa_Forn'         : 'Alerta: segurança de colisão do cambotador com o forno.'                             ,
    'Mesa_Posi'         : 'Alerta: segurança de colisão do cambotador com o forno.'                             ,
    'Camb_FornoMesa'    : 'Alerta: a mesa deve estar posicionada para o forno.'                                 ,
    'Camb_FornoMove'    : 'Alerta: o forno deve estar parado.'                                                  ,
    'Camb_PosiMesa'     : 'Alerta: a mesa deve estar posicionada para o posicionador.'                          ,
    'Camb_PosiMesaRec'  : 'Alerta: o posicionador deve estar com a mesa recuada.'                               ,
    'Camb_PosiMove'     : 'Alerta: o posicionador deve estar parado e fechado.'                                 ,
    'Posic_HomeMesaRe'  : 'Alerta: falha nos sensores de mesa recuada.'                                         ,
    'Posi_CambColis'    : 'Alerta: possível colisão com o cambotador embaixo, verifique as posições.'           ,
    'Posi_ReguColis'    : 'Alerta: possível colisão com a régua (recue a mesa ou abra a pinça).'                ,
    'Posic_MesaAvanc'   : 'Alerta: falha nos sensores de mesa avançada.'                                        ,
    'Posic_MesaRec'     : 'Alerta: falha nos sensores de mesa recuada.'                                         ,
    'Alim_FalhaSPFRam'  : 'Alerta: falta de pré-forma na rampa.'                                                ,
    'Alim_FalhaSPFRampa'  : 'Alerta: falta de pré-forma na rampa.'                                                ,
    'Alim_FaltaPFRamp'  : 'Alerta: nível baixo de pré-forma na rampa.'                                          ,
    'Alim_FaltaPFRampa'  : 'Alerta: nível baixo de pré-forma na rampa.'                                          ,
    'Alim_Descarregan'  : 'Alerta: aguarde até o forno ser descarregado.'                                       ,
    'PresComando_Alta'  : 'Alerta: pressão de comando acima de 7bar.'                                           ,
    'PresComando_Baix'  : 'Alerta: a pressão de comando ficou abaixo de 5bar.'                                  ,
    'PresSopro_Alta'    : 'Alerta: pressão de sopro acima do limite definido.'                                  ,
    'PresSopro_Baixa'   : 'Alerta: pressão de sopro abaixo do limite definido.'                                 ,
    'LinhaCheia'        : 'Alerta: sensor de linha cheia acionado.'                                             ,
    'FluxoH2O'          : 'Alerta: Fluxo de água não detectado, verifique alimentação de água.'                 ,
    'PortasAbertas'     : 'Alerta: Portas abertas.'                                                             ,
    'TorqueRegua'       : 'Alerta: sobretorque da régua detectado na saída de garrafas.'                        ,
    'OleoNivel'         : 'Alerta: Nível de óleo baixo.'                                                        ,
    'OleoPressao'       : 'Alerta: Pressão da bomba de óleo alta.'                                                        ,
    'TempMolde'         : 'Alerta: temperatura da água está acima do setpoint.'                                 ,
    'StatusFreio'       : 'Alerta: a mesa deve estar posicionada para o posicionador.'                          ,
    'Posi_CambColis'    : 'Alerta: possível colisão com o cambotador embaixo, verifique as posições.'           ,
    'AlimentacaoDePFn'  : 'Alerta: Pré forma travada verifique o alimentador'                                   ,
    'AlimentacaoDePFnoPino'  : 'Alerta: Pré forma travada verifique o alimentador'                                   ,
    'SegurancaRampa'    : 'Alerta: Falha de segurança na rampa, botão de emergência ou carenagem aberta.'       ,
    'TorquePrensa2'     : 'Alerta: Torque da prensa acima do limite definido.',
    'F0_Forno' :'Falha: erro no drive do forno.',
    'F1_Mesa' :   'Falha: erro no drive da Mesa.',
    'F2_Camb' :'Falha: erro no drive do cambotador.',
    'F3_Posic'    :   'Falha: erro no drive do posicionador.',
    'F4_Regua'    :   'Falha: erro no drive da régua.',
    'F5_Prensa'   :'Falha: erro no drive da prensa.',
    'F6_Estira'   :'Falha: erro no drive do estiramento.',
    'F7_ControlStop'  : 'Falha: Execução de Parada Controlada.',
    'F8_CS_Forno'     : 'Falha: parada Controlada do Forno (Verifique o Sinal X7 - Pino 4)',
    'F9_CS_Mesa'      : 'Falha: parada Controlada da Mesa(Verifique o Sinal X7 - Pino 4)',
    'F10_CS_Camb'     : 'Falha: parada Controlada do Cambotador (Verifique o Sinal X7 - Pino 4)',
    'F11_CS_Posic'    : 'Falha: parada Controlada do Posicionador (Verifique o Sinal X7 - Pino 4)',
    'F12_CS_Regua'    : 'Falha: parada Controlada da Régua (Verifique o Sinal X7 - Pino 4)',
    'F13_CS_Prensa'   : 'Falha: parada Controlada da prensa (Verifique o Sinal X7 - Pino 4)',
    'F14_CS_Estira'   : 'Falha: parada Controlada do Estiramento (Verifique o Sinal X7 - Pino 4)',
    'F15_OPStop'      : 'Falha: erro detectado em algum drive, verifique as demais falhas.',
    'F16_Emerg'       : 'Alerta: emergência da rampa detectada',
    'F17_ReleFase'    : 'Falha: parada por relé de fase, verifique a tensão do equipamento.',
    'F18_PortaAberta' : 'Falha: parada por portas abertas.',     
    'F19_PincaRegua1Fechada'  :  'Falha: o sensor de régua 1 deve estar desligado quando o cilindro está avançado.',
    'F20_PincaRegua1Aberta'   :  'Falha: o sensor de régua 1 deve estar ligado quando o cilindro está recuado.',
    'F21_PincaRegua2Fechada'  :  'Falha: o sensor de régua 2 deve estar desligado quando o cilindro está avançado.',
    'F22_PincaRegua2Aberta'    :'Falha: o sensor de régua 2 deve estar ligado quando o cilindro está recuado.',
    'F23_Bocal1UP': 'Falha: o sensor do bocal 1 deve estar desligado quando o cilindro está recuado.',
    'F24_Bocal1DW': 'Falha: o sensor do bocal 1 deve estar ligado quando o cilindro está avançado.',
    'F25_Bocal2UP': 'Falha: o sensor do bocal 2 deve estar desligado quando o cilindro está recuado.',
    'F26_Bocal2DW': 'Falha: o sensor do bocal 2 deve estar ligado quando o cilindro está avançado.',
    'F27_Bocal3UP': 'Falha: o sensor do bocal 3 deve estar desligado quando o cilindro está recuado.',
    'F28_Bocal3DW': 'Falha: o sensor do bocal 3 deve estar ligado quando o cilindro está avançado.',
    'F29_Bocal4UP': 'Falha: o sensor do bocal 4 deve estar desligado quando o cilindro está recuado.',
    'F30_Bocal4DW': 'Falha: o sensor do bocal 4 deve estar desligado quando o cilindro está recuado.',
    'F31_AvancMesaPosic': 'Falha: os sensores da mesa do posicionador avançado devem estar ligados quando o cilindro está avançado.',
    'F32_RecuaMesaPosic': 'Falha: falha nos sensores de mesa recuada.',
    'F33_SensorEstira': 'Falha: o sensor do estiramento deve estar ligado quando o mesmo estiver em cima.',  
    'F34_PFTorta': 'Falha: sensor de passagem de pré-forma acionado.',
    'F35_PressaoCmdBaixa': 'Falha: a pressão de comando ficou abaixo de 5bar.',
    'F36_PressaoCmdAlta': 'Falha: a pressão de comando ficou acima de 7bar.',
    'F37_PinFornoAbaixado;': 'Falha: sensor do pino do forno embaixo acionado. Verifique o sensor próximo a alimentação de preformas.',
    'F38_CambotadorColisao;': 'Falha: colisão entre cambotador e forno, verifique o conjunto.',
    'F39_PosicReguaColisao': 'Falha: colisão da posicionador e régua.',
    'F40_TorqueForno': 'Falha: sobretorque no forno.',
    'F41_ReguaPrensa': 'Falha: colisão da posicionador e régua.',
    'F42_EixosON': 'Falha: Os eixos não habilitaram corretamente.',                   
    'F43_FreioEsti': 'Falha: Freio do estiramento acionado',
    'F44_QuedaPF_no_preForno' : 'Falha: rotina de queda de preforma no pré-forno ativada, verifique o forno.',      
    'F45_CambForn': 'Falha: colisão entre cambotador e forno, verifique o conjunto.',
    'F46_CambRegu': 'Falha: colisão da posicionador e régua.'
    }

fault = {
    'F_Forno '              :'Falha: erro no drive do forno.',
    'F_Mesa'                :'Falha: erro no drive da Mesa.',
    'F_Camb'                :'Falha: erro no drive do cambotador.',
    'F_PosicUp'             :'Falha: erro no drive do posicionador Superior.',
    'F_PosicDw'             :'Falha: erro no drive do posicionador Inferior.',
    'F_Regua'               :'Falha: erro no drive da régua.',
    'F_Prensa'              :'Falha: erro no drive da prensa.',
    'F_Estira'              :'Falha: erro no drive do estiramento.',
    'StatusWord__Prensa'    :'Falha: erro no drive da prensa.',
	'StatusWord__Regua'     :'Falha: erro no drive da régua.',
	'StatusWord__Posic'     :'Falha: erro no drive do posicionador.',
	'StatusWord__Camb'      :'Falha: erro no drive do cambotador.',
	'StatusWord__Mesa'      :'Falha: erro no drive da Mesa.',
	'StatusWord__Forno'     :'Falha: erro no drive do forno.',
    'F_ControlStop'         :'Falha: Execução de Parada Controlada.',
    'F_CS_Forno'            :'Falha: parada Controlada do Forno (Verifique o Sinal X7 - Pino 4)',
    'F_CS_Mesa'             :'Falha: parada Controlada da Mesa(Verifique o Sinal X7 - Pino 4)',
    'F_CS_Camb'             :'Falha: parada Controlada do Cambotador (Verifique o Sinal X7 - Pino 4)',
    'F_CS_PosicUp'          :'Falha: parada Controlada do Posicionador superior (Verifique o Sinal X7 - Pino 4)',
    'F_CS_PosicDw'          :'Falha: parada Controlada do Posicionador Inferior (Verifique o Sinal X7 - Pino 4)',
    'F_CS_Regua'            :'Falha: parada Controlada da Régua (Verifique o Sinal X7 - Pino 4)',
    'F_CS_Prensa'           :'Falha: parada Controlada da prensa (Verifique o Sinal X7 - Pino 4)',
    'F_CS_Estira'           :'Falha: parada Controlada do Estiramento (Verifique o Sinal X7 - Pino 4)',
    'F_OPStop'              :'Falha: erro detectado em algum drive, verifique as demais falhas.',
    'F_Emerg'               :'Alerta: emergência da rampa detectada',
    'F_ReleFase'            :'Falha: parada por relé de fase, verifique a tensão do equipamento.',
    'F_PortaAberta'         :'Falha: parada por portas abertas.',                                                   
    'F_PincaRegua1Fechada'  :'Falha: o sensor de régua 1 deve estar desligado quando o cilindro está avançado.',
    'F_PincaRegua1Aberta'   :'Falha: o sensor de régua 1 deve estar ligado quando o cilindro está recuado.',
    'F_PincaRegua2Fechada'  :'Falha: o sensor de régua 2 deve estar desligado quando o cilindro está avançado.',
    'F_PincaRegua2Aberta'   :'Falha: o sensor de régua 2 deve estar ligado quando o cilindro está recuado.',
    'F_Bocal1UP'            :'Falha: o sensor do bocal 1 deve estar desligado quando o cilindro está recuado.',
    'F_Bocal1DW'            :'Falha: o sensor do bocal 1 deve estar ligado quando o cilindro está avançado.',
    'F_Bocal2UP'            :'Falha: o sensor do bocal 2 deve estar desligado quando o cilindro está recuado.',
    'F_Bocal2DW'            :'Falha: o sensor do bocal 2 deve estar ligado quando o cilindro está avançado.',
    'F_Bocal3UP'            :'Falha: o sensor do bocal 3 deve estar desligado quando o cilindro está recuado.',
    'F_Bocal3DW'            :'Falha: o sensor do bocal 3 deve estar ligado quando o cilindro está avançado.',
    'F_Bocal4UP'            :'Falha: o sensor do bocal 4 deve estar desligado quando o cilindro está recuado.',
    'F_Bocal4DW'            :'Falha: o sensor do bocal 4 deve estar desligado quando o cilindro está recuado.',
    'F_AvancMesaPosic'      :'Falha: os sensores da mesa do posicionador avançado devem estar ligados quando o cilindro está avançado.',
    'F_RecuaMesaPosic'      :'Falha: falha nos sensores de mesa recuada.',
    'F_SensorEstira'        :'Falha: o sensor do estiramento deve estar ligado quando o mesmo estiver em cima.',
    'F_PFTorta'             :'Falha: sensor de passagem de pré-forma acionado.',
    'F_PressaoCmdBaixa'     :'Falha: a pressão de comando ficou abaixo de 5bar.',
    'F_PressaoCmdAlta'      :'Falha: a pressão de comando ficou acima de 7bar.',
    'F_PinFornoAbaixado'    :'Falha: sensor do pino do forno embaixo acionado. Verifique o sensor próximo a alimentação de preformas.',
    'F_CambotadorColisao'   :'Falha: colisão entre cambotador e forno, verifique o conjunto.',
    'F_PosicReguaColisao'   :'Falha: colisão da posicionador e régua.',
    'F_TorqueForno'         :'Falha: sobretorque no forno.',
    'F_PosicReguaColisao'   :'Falha: colisão da posicionador e régua.',
    'F_QuedaPF_no_preForno' :'Falha: rotina de queda de preforma no pré-forno ativada, verifique o forno.',                                     
    'F_Camb_no_Forno'       :'Falha: colisão entre cambotador e forno, verifique o conjunto.'}

issues = [{'id': 'ffc09617-77ff-43e4-a971-eb8a9a689c6f', 'category': 'Alert', 'opened_at': '2024-02-28T08:43:37', 'closed_at': None, 'name': 'TorquePrensa2', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '22c3809c-6ca1-4525-af15-b38b59136895', 'category': 'Alert', 'opened_at': '2024-02-28T14:02:55', 'closed_at': '2024-02-28T14:03:05', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '93332ac9-f352-4633-8e06-dbd6edda67f8', 'category': 'Alert', 'opened_at': '2024-02-28T13:55:00', 'closed_at': '2024-02-28T13:55:10', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '1a90d0dd-2f82-4102-8c3b-941a9b27de63', 'category': 'Alert', 'opened_at': '2024-02-28T13:51:53', 'closed_at': '2024-02-28T13:52:04', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '392142d5-26a9-40ad-9e1d-6ad09d19b0e9', 'category': 'Alert', 'opened_at': '2024-02-28T13:49:58', 'closed_at': '2024-02-28T13:50:18', 'name': 'AlimentacaoDePFnoPino', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '4d70afe0-3c17-4681-91c7-dda21c03a6aa', 'category': 'Alert', 'opened_at': '2024-02-28T13:35:45', 'closed_at': '2024-02-28T13:35:55', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '89888815-a80f-4afc-a9cb-0e135c2fb016', 'category': 'Alert', 'opened_at': '2024-02-28T13:10:36', 'closed_at': '2024-02-28T13:10:46', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '9f0cee57-7926-4be6-863a-f8969cc48acb', 'category': 'Alert', 'opened_at': '2024-02-28T10:54:03', 'closed_at': '2024-02-28T13:00:13', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '9ff72da6-2414-421f-9033-494f863a1d15', 'category': 'Alert', 'opened_at': '2024-02-28T10:53:53', 'closed_at': '2024-02-28T13:00:13', 'name': 'Alim_FalhaSPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '8f82d206-9f72-48f5-8e42-0fbd355e7868', 'category': 'Alert', 'opened_at': '2024-02-28T10:00:34', 'closed_at': '2024-02-28T10:00:45', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': 'ad1883af-50d0-4129-9b47-f03b3729535c', 'category': 'Alert', 'opened_at': '2024-02-28T09:54:34', 'closed_at': '2024-02-28T09:54:44', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '51190ac0-2474-45c2-b5a0-cb831768e38e', 'category': 'Alert', 'opened_at': '2024-02-28T09:53:19', 'closed_at': '2024-02-28T09:53:30', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': 'fdd0057f-d12c-4334-9c21-a69e261719da', 'category': 'Alert', 'opened_at': '2024-02-28T08:59:49', 'closed_at': '2024-02-28T09:00:20', 'name': 'Alim_FalhaSPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '8fc3b6f1-c5ba-4b09-a7ef-f2178f886204', 'category': 'Alert', 'opened_at': '2024-02-28T08:59:39', 'closed_at': '2024-02-28T09:00:20', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '7e9a76ac-32fb-4dfa-818a-22568f99d5e1', 'category': 'Alert', 'opened_at': '2024-02-28T08:56:01', 'closed_at': '2024-02-28T08:56:12', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '5eb89101-437a-4924-82d8-c076d60f7267', 'category': 'Alert', 'opened_at': '2024-02-28T08:47:15', 'closed_at': '2024-02-28T08:47:36', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '3a77985c-2dd2-4b5e-96c5-00bed90b6388', 'category': 'Alert', 'opened_at': '2024-02-28T08:47:05', 'closed_at': '2024-02-28T08:47:15', 'name': 'Alim_FalhaSPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '28ec1363-11bf-4ed8-b6a9-0e882244fd63', 'category': 'Fault', 'opened_at': '2024-02-28T08:42:35', 'closed_at': '2024-02-28T08:42:45', 'name': 'F_Emerg', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': 'abd8b8b9-95b8-49a8-81a3-508e84e89e57', 'category': 'Fault', 'opened_at': '2024-02-28T08:42:35', 'closed_at': '2024-02-28T08:42:45', 'name': 'F_ReleFase', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '5b012d17-4673-4905-b04f-9e356c7a238e', 'category': 'Alert', 'opened_at': '2024-02-28T08:42:35', 'closed_at': '2024-02-28T08:42:45', 'name': 'PortasAbertas', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '2e36f602-dcd1-464b-a771-61e7417ceb3a', 'category': 'Alert', 'opened_at': '2024-02-28T07:04:54', 'closed_at': '2024-02-28T08:42:35', 'name': 'TorquePrensa2', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': 'ea3ed9cf-a80b-460a-9a0e-a6a109de92d8', 'category': 'Alert', 'opened_at': '2024-02-28T08:22:13', 'closed_at': '2024-02-28T08:23:46', 'name': 'TempMolde', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '95438d56-4e90-480b-a7b2-d129996eb9ef', 'category': 'Alert', 'opened_at': '2024-02-28T08:05:54', 'closed_at': '2024-02-28T08:06:04', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '7282401a-251b-4b7b-98a6-6c50add415d9', 'category': 'Alert', 'opened_at': '2024-02-28T08:00:51', 'closed_at': '2024-02-28T08:01:02', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '0fb03e8c-5bea-41ad-9b4f-e1a749458f05', 'category': 'Alert', 'opened_at': '2024-02-28T07:20:39', 'closed_at': '2024-02-28T07:21:00', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '95fc6c7a-9647-4dc0-a6df-53c31f5f1192', 'category': 'Alert', 'opened_at': '2024-02-28T07:20:18', 'closed_at': '2024-02-28T07:20:28', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': 'c7ca5d40-2628-424a-9d51-1256937f5a04', 'category': 'Alert', 'opened_at': '2024-02-28T07:04:54', 'closed_at': '2024-02-28T07:09:44', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '73361857-4ff8-4637-b436-96f8cd6631f0', 'category': 'Alert', 'opened_at': '2024-02-28T07:09:24', 'closed_at': '2024-02-28T07:09:34', 'name': 'Alim_FalhaSPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '7233c750-55cd-4577-89d8-2da4f9e9e59b', 'category': 'Alert', 'opened_at': '2024-02-28T07:05:04', 'closed_at': '2024-02-28T07:09:14', 'name': 'Alim_FalhaSPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '1f789f68-3b0b-4508-93e1-4451704c4705', 'category': 'Alert', 'opened_at': '2024-02-28T07:04:54', 'closed_at': '2024-02-28T07:06:59', 'name': 'PresSopro_Baixa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '84e36beb-535a-4733-9c49-cc9b52205b23', 'category': 'Alert', 'opened_at': '2024-02-27T17:00:45', 'closed_at': '2024-02-28T07:00:25', 'name': 'Alim_FalhaSPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': 'fccfc218-0d24-4a5a-8165-8d613154ae2b', 'category': 'Alert', 'opened_at': '2024-02-27T16:59:53', 'closed_at': '2024-02-28T07:00:25', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '629e6593-25a9-4fb4-a158-87fbd39650a9', 'category': 'Alert', 'opened_at': '2024-02-27T13:11:03', 'closed_at': '2024-02-28T07:00:25', 'name': 'TorquePrensa2', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '48f8491d-5c50-43ee-a5c0-29ffb868ca09', 'category': 'Alert', 'opened_at': '2024-02-27T16:59:32', 'closed_at': '2024-02-27T17:00:34', 'name': 'Alim_FalhaSPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '9074c98a-3cad-42d0-8b61-82a619e0cbee', 'category': 'Alert', 'opened_at': '2024-02-27T16:59:22', 'closed_at': '2024-02-27T16:59:32', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': 'a323c17e-e7d9-4c85-a53e-7a89d5ef6cba', 'category': 'Alert', 'opened_at': '2024-02-27T16:43:28', 'closed_at': '2024-02-27T16:43:38', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': 'daf198f5-df92-4ed7-acbc-eba171fa4f59', 'category': 'Alert', 'opened_at': '2024-02-27T16:43:07', 'closed_at': '2024-02-27T16:43:17', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '446281fe-5c5a-4c5a-b8b4-6a57a139d8f3', 'category': 'Alert', 'opened_at': '2024-02-27T16:25:27', 'closed_at': '2024-02-27T16:25:48', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': 'ba6c5d55-68c5-4b7c-9c21-3f299760631e', 'category': 'Alert', 'opened_at': '2024-02-27T16:02:15', 'closed_at': '2024-02-27T16:02:25', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '4ef2f5fd-90e6-4a9a-b47d-23e29ac97da9', 'category': 'Alert', 'opened_at': '2024-02-27T16:00:10', 'closed_at': '2024-02-27T16:00:20', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': 'e388a36e-d5fc-45cb-b903-9f3f19753bfd', 'category': 'Alert', 'opened_at': '2024-02-27T15:52:13', 'closed_at': '2024-02-27T15:52:33', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '83adbd2b-f270-4809-b153-ddb450216187', 'category': 'Alert', 'opened_at': '2024-02-27T15:09:26', 'closed_at': '2024-02-27T15:09:37', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': 'f5478e27-a08f-44ca-a75c-0aef7be076fa', 'category': 'Alert', 'opened_at': '2024-02-27T14:53:32', 'closed_at': '2024-02-27T14:53:42', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': '5e347c58-234b-4a85-a9bc-f95ffa9e466f', 'category': 'Alert', 'opened_at': '2024-02-27T14:41:03', 'closed_at': '2024-02-27T14:41:14', 'name': 'Alim_FaltaPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}, {'id': 'd7df338e-ca32-4d6e-b707-0a4e445cbaf7', 'category': 'Alert', 'opened_at': '2024-02-27T14:28:24', 'closed_at': '2024-02-27T14:28:34', 'name': 'Alim_FalhaSPFRampa', 'device': '5579bf4d-beee-4c18-ab15-996faa8743db'}]

def process_issues(issues):
    df = pd.DataFrame(issues)
    df['name'] = df['name'].map(alert).fillna(df['name'])
    df['name'] = df['name'].map(fault).fillna(df['name'])
    df["opened_at"] = pd.to_datetime(df["opened_at"])
    df = df[["opened_at", "name"]]

    off_limit = pd.Timedelta(minutes=3)
    df = df.sort_values(by=['name','opened_at'], ascending=True)
    df['diff'] = df['opened_at'].diff()
    print(df)
    df.reset_index(drop=True, inplace=True)
    rows_to_remove = []

    for i in range(1, len(df)):
        if df.iloc[i]['name'] == df.iloc[i - 1]['name']:
            if df.iloc[i]['diff'] < pd.Timedelta(minutes=15):
                rows_to_remove.append(i)

    result = df.drop(rows_to_remove)
    result.reset_index(drop=True, inplace=True)
    result = result.sort_values(by=['opened_at'], ascending=True)
    result["opened_at"] = pd.to_datetime(result["opened_at"]).dt.strftime('%d/%m %H:%M')
    result = result[["opened_at", "name"]]
    result.columns = ["Hora",  "Nome"]
    return result 

print(process_issues(issues))