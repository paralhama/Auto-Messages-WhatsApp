from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pyperclip
from selenium.webdriver.common.action_chains import ActionChains
import PySimpleGUI as sg
from time import sleep
import phonenumbers
from subprocess import CREATE_NO_WINDOW

icon = 'icon.ico'
numero = ''
mensagem = ''
exemplo_aberto = False
conectando_numero = None

service = Service(ChromeDriverManager().install())
service.creation_flags = CREATE_NO_WINDOW
options = Options()
options.add_argument("--log-level=OFF")
options.add_argument("--window-position=-2000,-2000")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
navegador = webdriver.Chrome(service=service, options=options)


def theme():
    sg.theme('DarkTeal11')
    sg.theme_text_color('white')


def janela_inserir_numero():
    theme()
    layout = [
        [sg.Text('Conecte seu aparelho!', font=(20, 20))],
        [sg.Text('Insira o DDD e o número de telefone\n', font=(20, 20))],

        [sg.InputText(key='numero',
                      focus=True,
                      font=(30, 30),
                      size=13,
                      justification='center',
                      border_width=0,
                      change_submits=True,
                      pad=20)],

        [sg.Text('',
                 key='msg_numero_invalido',
                 background_color='#405559',
                 text_color='red',
                 font=(20, 20))],

        [sg.Button('Enviar código de ativação',
                   font=(20, 20),
                   disabled=True, pad=20,
                   key='botão_enviar_código_ativação')]

    ]

    return sg.Window('Auto Messages WhatsApp', layout=layout, finalize=True, element_justification='center',
                     icon=icon, size=(500, 350))


def janela_codigo_ativacao():
    global conectando_numero
    navegador.get("https://web.whatsapp.com/")
    wait = WebDriverWait(navegador, 10)

    # Verifica se o link 'Conectar com número de telefone' esta disponível
    codigo_ativacao = wait.until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[3]/div[1]/div/div/div[3]/div/span')))
    if codigo_ativacao.is_displayed():
        codigo_ativacao.click()

    # Verifica se o campo de digitação do número está disponível
    digitar_numero = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="app"]/div/div/div[3]/div[1]/div/div[3]/div[2]/div/div/div/form/input')))
    if digitar_numero.is_displayed():
        digitar_numero.click()
        digitar_numero.send_keys(numero)
        sleep(2)
        # Clicar no botão 'Enviar'
        navegador.find_element('xpath',
                               '//*[@id="app"]/div/div/div[3]/div[1]/div/div[3]/div[3]/div/div/div').click()

    campo1 = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="app"]/div/div/div[3]/div[1]/div/div/div[2]/div/div/div/div[1]/span')))
    if campo1.is_displayed():
        campo1 = campo1.text
        campo2 = navegador.find_element('xpath',
                                        '//*[@id="app"]/div/div/div[3]/div[1]/div/div/div[2]/div/div/div/div[2]/span').text
        campo3 = navegador.find_element('xpath',
                                        '//*[@id="app"]/div/div/div[3]/div[1]/div/div/div[2]/div/div/div/div[3]/span').text
        campo4 = navegador.find_element('xpath',
                                        '//*[@id="app"]/div/div/div[3]/div[1]/div/div/div[2]/div/div/div/div[4]/span').text
        campo5 = navegador.find_element('xpath',
                                        '//*[@id="app"]/div/div/div[3]/div[1]/div/div/div[2]/div/div/div/div[5]/span').text
        campo6 = navegador.find_element('xpath',
                                        '//*[@id="app"]/div/div/div[3]/div[1]/div/div/div[2]/div/div/div/div[6]/span').text
        campo7 = navegador.find_element('xpath',
                                        '//*[@id="app"]/div/div/div[3]/div[1]/div/div/div[2]/div/div/div/div[7]/span').text
        campo8 = navegador.find_element('xpath',
                                        '//*[@id="app"]/div/div/div[3]/div[1]/div/div/div[2]/div/div/div/div[8]/span').text
        codigo_ativacao = f" {campo1} {campo2} {campo3} {campo4} - {campo5} {campo6} {campo7} {campo8} "
        conectando_numero = navegador.find_element('xpath',
                                                   '//*[@id="app"]/div/div/div[3]/div[1]/div/div/div[1]/div[2]').text
        conectando_numero = conectando_numero.replace("+55 ", "").replace(" (Editar)", "")

    theme()
    layout = [
        [sg.Text('Insira o código no seu celular', font=(20, 20), pad=(0, 10))],
        [sg.Text(codigo_ativacao, key='código', font=(30, 30), background_color='#52DE97', text_color='black')],
        [sg.Text('\n')],
        [sg.Text(conectando_numero, font=(15, 15))],
        [sg.Button('Editar número / Gerar novo código', pad=0, font=(15, 15))]
    ]

    return sg.Window(f'Auto Messages WhatsApp', layout=layout, finalize=True, element_justification='center',
                     icon=icon, size=(550, 250))


def janela_mensagem():
    numero_formatado = f'{numero[:2]} {numero[2:7]}-{numero[7:]}'

    theme()
    layout = [
        [sg.Text('\nDigite sua mensagem:', font=30)],
        [sg.Multiline(size=(60, 10), key='mensagem', font=(15, 15))],
        [sg.Button('Próximo passo', font=15)],
        [sg.Text(f'\nConectado ao WhatsApp: {numero_formatado}', key='numero_conectado', font=15)],
        [sg.Button('Editar número', font=10)]
    ]
    return sg.Window('Auto Messages WhatsApp', layout=layout,
                     finalize=True, element_justification='center', icon=icon, size=(700, 450))


def janela_exemplo():
    theme()
    layout = [
        [sg.Text('Adicione os números, nomes e grupos seguindo o exemplo abaixo:', font=20)],
        [sg.Multiline('11940028922\n'
                      '11940000103\n'
                      'Lucas\n'
                      'Erik Mendes\n'
                      'Grupo do trabalho\n'
                      'Grupo da família\n', disabled=True, size=(40, 10), font=20)],
        [sg.Text('Se algum número, nome ou grupo não for identificado no seu Whatsapp', font=20)],
        [sg.Text('O destinatário será desconsiderado', font=20)],
        [sg.Button('Adicionar destinatários', font=20)]
    ]

    return sg.Window('ATENÇÃO!', layout=layout, finalize=True, element_justification='center', no_titlebar=True,
                     keep_on_top=True)


def janela_contatos():
    theme()
    layout = [
        [sg.Text('Informe os destinatários:', font=20)],
        [sg.Multiline(size=(50, 10), key='lista_contatos', font=20, change_submits=True)],
        [sg.Button('Editar mensagem', font=20), sg.Button('Enviar', font=20)],
        [sg.Text('\n')],
        [sg.Button('Exibir exemplo novamente', font=20)]
    ]
    return sg.Window('Auto Messages WhatsApp', layout=layout, finalize=True,
                     icon=icon, element_justification='center', size=(500, 420))


def verificar_login():
    login = None
    try:
        """
        Verifica se a foto de perfil do usuário apareceu, se apareceu retorna True
        indicando que o login foi feito com sucesso"""
        codigo = navegador.find_element('xpath', '//*[@id="app"]/div/div/div[4]/header/div[1]/div/img')
        login = True
    except NoSuchElementException:
        login = False
    return login


def enviar_mensagem(mensagem, lista_de_contatos):
    elemento = None
    wait = WebDriverWait(navegador, 10)

    # Verifica se a tela inicial foi carregada verificando se o campo de busca de contatos foi carregado.
    campo_de_busca = wait.until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p')))
    if campo_de_busca.is_displayed():
        navegador.find_element('xpath', '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p').click()
        navegador.find_element('xpath', '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p').send_keys(
            lista_de_contatos[0])
        navegador.find_element('xpath', '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p').send_keys(Keys.ENTER)
        sleep(1)

        pyperclip.copy(mensagem)
        navegador.find_element('xpath',
                               '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div[2]/div[1]/p').send_keys(
            Keys.CONTROL + 'v')
        sleep(1)
        navegador.find_element('xpath',
                               '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div[2]/div[1]/p').send_keys(
            Keys.ENTER)
        sleep(2)

    mensagens_na_tela = navegador.find_elements('class name', '_2AOIt')
    for item in mensagens_na_tela:
        if mensagem.replace("\n", "") in item.text.replace("\n", ""):
            elemento = item
            break

    ActionChains(navegador).move_to_element(elemento).perform()
    elemento.find_element('class name', '_3u9t-').click()

    # clicar no botão 'encaminhar'
    navegador.find_element('xpath', '//*[@id="app"]/div/span[4]/div/ul/div/li[4]/div').click()
    # clicar no ícone 'encaminhar'
    navegador.find_element('xpath', '//*[@id="main"]/span[2]/div/button[4]/span').click()

    for index, contato in enumerate(lista_de_contatos):
        if contato != lista_de_contatos[0]:
            sleep(1)
            pyperclip.copy(lista_de_contatos[index])
            navegador.find_element('xpath',
                                   '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div/div[1]/p').send_keys(
                Keys.CONTROL + 'v')
            sleep(1)
            navegador.find_element('xpath',
                                   '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div/div[1]/p').send_keys(Keys.ENTER)
            sleep(1)

            navegador.find_element('xpath',
                                   '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div/div[1]/p').send_keys(Keys.CONTROL + 'A')

            navegador.find_element('xpath',
                                   '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/div[1]/div/div/div[2]/div/div[1]/p').send_keys(Keys.BACKSPACE)

    sleep(0.5)
    navegador.find_element('xpath',
                           '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/span/div/div/div/span').click()


def desconectar_whatsapp():
    wait = WebDriverWait(navegador, 10)
    options_disconnect = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="app"]/div/div/div[4]/header/div[2]/div/span/div[4]/div/span')))
    if options_disconnect.is_displayed():
        options_disconnect.click()

    disconnect = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="app"]/div/div/div[4]/header/div[2]/div/span/div[4]/span/div/ul/li[6]/div')))
    if disconnect.is_displayed():
        disconnect.click()

    confirmar = wait.until(EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div[3]/div/button[2]/div/div')))
    if confirmar.is_displayed():
        confirmar.click()


janela1 = janela_inserir_numero()
janela2 = None
janela3 = None
janela4 = None
janela5 = janela_contatos()
janela5.hide()

while True:
    try:
        login = verificar_login()
        window, event, values = sg.read_all_windows(timeout=1000)
        if window == janela1:  # Janela para inserir número
            if event == sg.WINDOW_CLOSED:
                navegador.quit()
                break

            if not str(values['numero']).isnumeric():
                window['numero'].update(values['numero'][:-1])

            if len(values['numero']) == 12:
                window['numero'].update(values['numero'][:-1])

            if len(values['numero']) >= 11:
                checar_numero = phonenumbers.parse('+55' + values['numero'])
                checar_numero = phonenumbers.is_valid_number(checar_numero)
                if checar_numero:
                    window['botão_enviar_código_ativação'].update(disabled=False)
                    window['msg_numero_invalido'].update(visible=False)
                else:
                    window['msg_numero_invalido'].update('Insira um número de telefone válido')

            if len(values['numero']) < 11:
                window['botão_enviar_código_ativação'].update(disabled=True)
                window['msg_numero_invalido'].update(visible=True)
                window['msg_numero_invalido'].update('')

            if event == 'botão_enviar_código_ativação':
                sg.popup_no_buttons('Aguarde: gerando código de ativação...',
                                    auto_close=True,
                                    non_blocking=True,
                                    keep_on_top=True,
                                    no_titlebar=True,
                                    font=(15, 15))
                numero = values['numero']
                janela1.hide()
                janela2 = janela_codigo_ativacao()

        if login == True and janela2 is not None:
            janela2.close()
            janela2 = None
            sg.popup_no_buttons('WhatsApp conectado com sucesso!',
                                auto_close=True,
                                non_blocking=True,
                                keep_on_top=True,
                                no_titlebar=True,
                                font=(15, 15))
            sleep(3)
            janela3 = janela_mensagem()
            login = False
            window, event, values = sg.read_all_windows()

        if window == janela2:  # Janela que exibe código de ativação
            if event == sg.WINDOW_CLOSED:
                sair = sg.popup('Você tem certeza que deseja sair?\n'
                                'Ao sair, todos os processos e informações serão perdidos.',
                                custom_text=('Sim', 'Não'), no_titlebar=True, keep_on_top=True)
                if sair == 'Sim':
                    navegador.quit()
                    break

            if event == 'Editar número / Gerar novo código':
                janela2.hide()
                janela1.un_hide()

        if window == janela3:  # Janela para o usuário digitar a mensagem
            if event == sg.WINDOW_CLOSED:
                sair = sg.popup('Você tem certeza que deseja sair?\n'
                                'Ao sair, todos os processos e informações serão perdidos.',
                                custom_text=('Sim', 'Não'), no_titlebar=True, keep_on_top=True)
                if sair == 'Sim':
                    navegador.quit()
                    break

            if event == 'Editar número':
                desconectar = sg.popup('Você tem certeza que deseja conectar outro número?',
                                       custom_text=('Sim', 'Não'), no_titlebar=True, keep_on_top=True)
                if desconectar == 'Sim':
                    desconectar_whatsapp()
                    login = False
                    janela3.hide()
                    janela1.un_hide()

            if event == 'Próximo passo':
                if len(values['mensagem']) == 0:
                    sg.Popup('Sua mensagem esta vazia!\n'
                             'Digite uma mensagem para continuar', no_titlebar=True, keep_on_top=True)
                else:
                    mensagem = values['mensagem']
                    janela3.hide()
                    if not exemplo_aberto:
                        janela4 = janela_exemplo()
                    else:
                        janela5.un_hide()

        if window == janela4:  # Janela que exibe como o usuário deve digitar os destinatários
            if event == sg.WINDOW_CLOSED or event == 'Adicionar destinatários':
                janela4.hide()
                janela5.un_hide()
                exemplo_aberto = True

        if window == janela5:  # Janela para o usuário digitar os destinatários
            if event == sg.WINDOW_CLOSED:
                sair = sg.popup('Você tem certeza que deseja sair?\n'
                                'Ao sair, todos os processos e informações serão perdidos.',
                                custom_text=('Sim', 'Não'), no_titlebar=True, keep_on_top=True)
                if sair == 'Sim':
                    navegador.quit()
                    break

            if event == 'Enviar':
                if len(values['lista_contatos']) == 0:
                    sg.Popup('Por favor, insira um ou mais destinatários para continuar.',
                             no_titlebar=True, keep_on_top=True)
                else:
                    lista_contatos = []
                    for contato in str(values['lista_contatos']).split('\n'):
                        lista_contatos.append(contato.strip())
                    contatos = lista_contatos
                    janela5.hide()
                    sg.popup_no_buttons('Aguarde: enviando mensagens...',
                                        auto_close=True,
                                        non_blocking=True,
                                        keep_on_top=True,
                                        no_titlebar=True,
                                        font=(15, 15))
                    enviar_mensagem(mensagem, contatos)
                    sg.popup_no_buttons('Mensagens enviadas com sucesso!',
                                        auto_close=True,
                                        non_blocking=True,
                                        keep_on_top=True,
                                        no_titlebar=True,
                                        font=(15, 15), auto_close_duration=3)
                    sleep(3)
                    janela5.un_hide()

            if event == 'Editar mensagem':
                janela5.hide()
                janela3.un_hide()

            if event == 'Exibir exemplo novamente':
                janela5.hide()
                janela4.un_hide()
    except NoSuchWindowException:
        break
