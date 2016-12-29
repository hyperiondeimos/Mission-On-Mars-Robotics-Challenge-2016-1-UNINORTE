# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 02:19:45 2016

@author: Anderson Gadelha Fontoura
"""

# com ajuda do Phd Adrian Rosebrock do blog http://www.pyimagesearch.com

# pacotes necessários
from collections import deque
import numpy as np
import argparse
import imutils
import time
import cv2
from imutils.video import WebcamVideoStream
import serial as sp
import datetime

class VideoStream:
	def __init__(self, src=0, usePiCamera=False, resolution=(320, 240),
		framerate=32):
		# checa se a picamera pode ser usada...
		if usePiCamera:
			# importar os pacotes da picamera a menos que nós
			# explicitamente falamos -- isso ajuda a remover o requerimento
			# 'picamera[array]' dos PCs e notebooks
			# que continuam a usar o pacote 'imutils'
			from pivideostream import PiVideoStream

			# inicializa a picamera e permite ao sensor se preparar (IR)
			self.stream = PiVideoStream(resolution=resolution,
				framerate=framerate)

		# caso contrário, se vamos usar o OpenCV, então inicializamos a transmissão da webcam
		else:
			self.stream = WebcamVideoStream(src=src)

	# funções do warm-up

	def start(self):
		# inicia a thread da transmissão de video
		return self.stream.start()

	def update(self):
		# pega o próximo frame da transmissão
		self.stream.update()

	def read(self):
		# retorna o frame atual
		return self.stream.read()

	def stop(self):
		# para a thread e libera a camera
		self.stream.stop()

#funçao para capturar a imagem
def getImage():
	retval, im = camera.read()
	return im

# construi o analisador de argumento para realizar a passagem de parametros
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="caminho para o (opcional) arquivo de video")
ap.add_argument("-b", "--buffer", type=int, default=32,
    help="max buffer size")
args = vars(ap.parse_args())

# para o picamera descomente as linhas 68 a 73

# construi o analisador de argumento para realizar a passagem de parametros

#ap = argparse.ArgumentParser()
#ap.add_argument("-p", "--picamera", type=int, default=-1,
#	help="Com ou sem a picamera, o processo deve ser iniciado")
#ap.add_argument("-b", "--buffer", type=int, default=32,
#    	help="max buffer size")
#args = vars(ap.parse_args())

# inicializa a transmissão do video e permite que o sensor da camera se prepare para verificar o foco
#camera = VideoStream(usePiCamera=args["picamera"] > 0).start()
#time.sleep(2.0)

# Comunicação Serial via Arduino

#ser = sp.Serial('/dev/ttyUSB0', 9600, timeout = 1) # Linux (Raspberry) e OSX
ser = sp.Serial('/dev/ttyACM0', 9600)	# Linux (Raspberry) e OSX
#ser = sp.Serial('COM14', 9600, timeout = 0) # Windows
ser.close() #Fecha a porta
ser.open() # abre a porta

# define o limite inferior e superior do verde no espaço de cor HSV
# bola no HSV
# green-yellow 173-255-47
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
#greenUpper = (64, 255, 255)

# inicializa a lista dos pontos seguidos, o contador de frames, e as coordenadas deltas
pts = deque(maxlen=args["buffer"])	# o deque irá manter as coordenadas
#pts = deque(maxlen=args["picamera"])
counter = 0
(dX, dY) = (0, 0)
direction = ""

# Se o diretorio de video não for passado, pega a referencia da webcam mesmo
# comente daqui (98) até a '!' se estiver usando a PiCamera
if not args.get("video", False):
    camera = cv2.VideoCapture(0) #0, 1, 2,... são as cameras. Se só tiver uma camera, coloque apenas 0.

# caso contrário, pega a referencia de um arquivo de video
else:
    camera = cv2.VideoCapture(args["video"])

# !

# Loop infinito
while True:
    # pega o frame atual
    (grabbed, frame) = camera.read()

    # se estivermos vendo um video e nós não pegamos um unico frame, logo atingimos o fim do arquivo de video
    if args.get("video") and not grabbed:
        break

    # redimensiona o frame (para ser mais rápido o processamento, borramos a imagem e convertemos no espaço de cor HSV
    frame = imutils.resize(frame, width=600)	#redimensiona a coordenada X (se quiser mexer na Y coloque ',height = XXX')
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)  #bora a imagem (isto facilita 'enxergar' o contorno do objeto)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #mua de RGB para HSV (para a tratativa da imagem)

    # constroi uma mascara para a cor verde (pode ser outra cor se quiser), então faz uma serie de dilatações e erosões para remover
    # os 'blobs' de pixels que ficam na máscara
    mask = cv2.inRange(hsv, greenLower, greenUpper) #criação da mascara para o verde - isto binariza a imagem
    mask = cv2.erode(mask, None, iterations=2) #cria a erosão na forma 'verde' enxergada pela camera 
    mask = cv2.dilate(mask, None, iterations=2) #dilata a forma 'verde' na camera

    # encontra os contornos da mascara e inicializa o valores atuais de (x,y), que é o centro da bola
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # apenas continua se pelo menos um contorno foi encontrado
    if len(cnts) > 0 and ser:
        # encontra o maior contorno na mascara (isto impede que duas bolas possam ser lidas de forma simultaneas na imagem)
        # Então use isto para computar um circulo minimo que irá contornar o centroide da bola
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        #center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        
		#M["m10"] coordenada geral de x
		#M["m01"] coordenada geral de y
		#M["m00"] area analisada

        cX = int(M["m10"] / M["m00"]) # coordenada real de x
        cY = int(M["m01"] / M["m00"]) # coordenada real de y
        
        center = (cX, cY) #centroide
                
        #manda a informação para o arduino e printa na tela as coordenadas        
        print('x: ', cX, '; y: ', cY)
        
    
    	# se a bola aparecer a esquerda da camera e no alto, manda a info para virar para a esquerda
        if cX < 200 and cY < 300:
            rs = 'l'
	    	print('l')            
                	
    	# se a bola aparecer a direita da camera e no alto, manda a info para virar para a direita
        if cX > 410 and cY < 300:
	    	rs = 'r'
            print('r')

        # se a bola aparecer no centro da camera e no alto, manda a info para seguir em frente
        if cX >= 200 and cX <= 400 and cY < 300:
            rs = 'c'
        	print('c')	
	
        # se a bola estiver bem próxima e se deslocar para baixo da camera, manda a info para parar e tira uma foto do lugar
        if cY > 300:
            rs = 'f'
            ramp_frames = 30 #numero de frames jogados para ajuste de iluminação
            for i in xrange(ramp_frames):
 				temp = get_image()
 			camera_capture = get_image()
 			file = datetime.datetime.now() #recebe a hora e data atuais 
 			direc = "/home/pi/" #onde irá salvar a imagem
 			cv2.imwrite(direc + file + ".png", camera_capture) #nome da imagem será data + horário + .png  
        	print('f')

	coman = ser.read()
	if coman == 't':
		ser.write(rs)
        
        # apenas procede se o raio da forma da bola atinge um tamanho minimo
        if radius > 10:
            # desenha um circulo e o centroide no frame e atualiza os pontos de rastreio
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            pts.appendleft(center)
    
    # caso contrário, se a bola sair ou nao estiver no frame, manda a info de processo automatico do arduino        
    else:
        cX = -10;
        cY = -10;
        print('x: ', cX, '; y: ', cY)
        rs = 'a'        
        print('a')

	#time.sleep(0.5)        
    coman = ser.read()   
    if coman == 't':
        ser.write(rs)
    	

    # faz um loop sobre os pontos monitorados
    for i in np.arange(1, len(pts)):
        # se qualquer dos pontos monitorados for igual a NONE, ignore 
        # logo
        if pts[i - 1] is None or pts[i] is None:
            continue

        # checa se existe pontos suficientes para serem acumulados no buffer
        #if counter >= 10 and i == 1 and pts[-10] is not None:
        if counter >= 10 and i == 1 and len(pts) == args["buffer"]:        
            # computa a diferença entre as coordenadas x e y. E reinicia as variaveis de direção no texto
            dX = pts[i-10][0] - pts[i][0]
            dY = pts[i-10][1] - pts[i][1]
            #dxp = pts[i][0]
            #dyp = pts[i][1]
            (dirX, dirY) = ("", "")

            # garante que existe um movimento significante na direção X
            if np.abs(dX) > 20:
                dirX = "Leste" if np.sign(dX) == 1 else "Oeste"

            # garante que existe um movimento significante na direção Y
            if np.abs(dY) > 20:
                dirY = "Norte" if np.sign(dY) == 1 else "Sul"

            # cuida para que ambas as direções não sejam vazias
            if dirX != "" and dirY != "":
                direction = "{}-{}".format(dirY, dirX)

            # caso contrário, apenas uma direção não é vazia
            else:
                direction = dirX if dirX != "" else dirY

        # caso contrário, computa a grossura da linha e conecta os pontos e forma uma linha de rastreio
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # mostra o movimento dos deltas e a direção do movimento no frame
    #cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
    #    0.65, (0, 0, 255), 3)
    #cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
    #    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
    #    0.35, (0, 0, 255), 1)
    
    # mostra o frame da camera em uma janela e incrementa o contador de frame.
    #cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    counter += 1
        
    # se a tecla 'q' for pressionada, para tudo
    if key == ord("q"):
        break

# libera a camera e fecha todas as conexões e janelas ativas
camera.release()
ser.close()
cv2.destroyAllWindows()