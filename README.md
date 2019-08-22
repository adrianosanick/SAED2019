# SAED
## Sistena de Aquisição Eletrônica de Dados

Descrição do Sistema:

- Resolução do conversor ADC: 10bits
- Tensão de Ref+ do ADC: 3.3V
- Tensão de Ref- do ADC: 0V
- Non-Linearity Típica do sensor LM35: ±¼°C

**Cálculo do Erro teórico do SAED**

ErroTeórico = Erro_resoluçãoADC + ErroLM35

- Erro_resoluçãoADC =  ((3.3-0)/1024)) / 0.01 = 0.32°C
- ErroLM35 = 0.25°C

## ErroTeórico= ±0.57°C

