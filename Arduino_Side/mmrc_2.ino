#include <Servo.h> // importando biblioteca de servo motor
#include <Ultrasonic.h> // importando biblioteca do ultrassonico
#include <AFMotor.h> // import da lib Motor Shield

#define pinoRecep 7 // definindo pino de recepcao do ultrassonico (pin_echo)
#define pinoEmiss 6 // definindo pino de emissão do ultrassonico (pin_trigger)

#define SERVO1_PWM 10 //Servo 1 na shield

AF_DCMotor motor1(1); //esquerda
AF_DCMotor motor2(4); //direita

const int velocidade = 200; // velocidade 0-255
//int inByte = 0; //recebe byte pela Serial
char inByte[10];
const float velang = 16.7; // definindo velocidade angular media 16,7ms por grau
//String inputString = "";         // string usada para guardar (buffer) da porta serial
boolean left = false, right = false, center = false, ans = false, front = false, stringComplete = false;


Servo servo; // cria um objeto Servo
Ultrasonic ultra(pinoEmiss, pinoRecep); // criando um objeto ultrassonico

void setup() {
  Serial.begin(9600);
  pinMode(pinoEmiss, OUTPUT);
  pinMode(pinoRecep, INPUT);
  servo.attach(SERVO1_PWM); // relacionando servo físico com virtual
  //inputString.reserve(10);
  delay(3000); // delay p/ posicionar o robô
  motor1.setSpeed(200);
  motor2.setSpeed(200);
  motor1.run(RELEASE);
  motor2.run(RELEASE);
}

//loop principal
void loop() {
  //delay(500);
  establishContact();
  //se houver resposta do raspberry
  char T = receiveContact();
  //if (stringComplete) {
  // se o sinal recebido for 'l', vira para a esquerda
  if (T == 'l') {
    //delay(100);
    motor1.run(RELEASE);
    motor2.run(FORWARD);
    motor1.setSpeed(0);
    motor2.setSpeed(200);
    Serial.flush(); //limpa a porta
    stringComplete = false; //nega o envio
    left = false; //nega a ida a esquerda
  }

  //se for recebido 'c', segue em frente
  if (T == 'c') {
    //delay(100);
    motor1.run(FORWARD);
    motor2.run(FORWARD);
    motor1.setSpeed(200);
    motor2.setSpeed(200);
    Serial.flush();
    stringComplete = false;
    center = false; // nega a ida em frente
  }
  // se for recebido 'r', vira a direita
  if (T == 'r') {
    //delay(100);
    motor1.setSpeed(200);
    motor2.setSpeed(0);
    motor1.run(FORWARD);
    motor2.run(RELEASE);
    Serial.flush();
    stringComplete = false;
    right = false; //nega a direita
  }
  // se for recebido 'a', o arduino fica autonomo
  if (T == 'a') {
    //delay(200);
    autoArd();
    Serial.flush();
    stringComplete = false;
    ans = false; //nega o sinal autonomo
  }
  // se for recebido 'f', significa que a bola está bem na frente do robo - anda um pouco e para por 3s
  if (T == 'f') {
    //delay(100);
    motor1.run(FORWARD);
    motor2.run(FORWARD);
    motor1.setSpeed(150);
    motor2.setSpeed(150);
    delay(1000);
    motor1.run(RELEASE);
    motor2.run(RELEASE);
    motor1.setSpeed(0);
    motor2.setSpeed(0);
    delay(3000); //parada de 3s
    Serial.flush();
    T = 'z';
    stringComplete = false;
    front = false; //nega que a bola esteja na frente.
  }
  //  } else {
  //    autoArd();
  //    Serial.flush();
  //    inputString = "";
  //  }
}

// função automatica do Arduino para a leitura do sensor ultrassonico
void autoArd() {
  //int distancia = 0; // "limpa" a varíavel
  //delayMicroseconds(10); // espera 5 microsegundos
  //float distancia;
  //long microsec = ultrasonic.timing();
  //distancia = ultrasonic.convert(microsec, Ultrasonic::CM);
  int distancia = ultra.Ranging(CM); // calculando distancia em cm
  delayMicroseconds(10); // espera 5 microsegundos
  Serial.println(distancia);
  if (distancia >= 30 || distancia == 0) {
    motor1.run(FORWARD);
    motor2.run(FORWARD);
    motor1.setSpeed(200);
    motor2.setSpeed(200);
    }
  else if (distancia < 30 && distancia > 0) {
    motor1.run(RELEASE);
    motor2.run(RELEASE);
    motor1.setSpeed(0);
    motor2.setSpeed(0);
    Busca(); //chama funcao Busca
    }
}

// função busca (vai procurar por um caminho sem obstáculos)
void Busca() {
  servo.write(15); // servo vira para 15 graus
  delay(2000);
  int distancia = ultra.Ranging(CM);
  Serial.print(distancia);
  if (distancia >= 40) {
    servo.write(90);
    viraresquerda(90); // vira 90 graus pra esquerda
    delay(100);
  }
  else if (distancia < 40) {
    servo.write(165); // servo vira para 165 graus
    delay(2000);
    distancia = ultra.Ranging(CM);
    if (distancia >= 40) {
      servo.write(90);
      virardireita(70); //vira 90 graus pra direita
      delay(100);
    }
    if (distancia < 40) {
      servo.write(90);
      meiavolta(); //chama função meiavolta
      delay(100);
    }
  }
}

// função para virar a esquerda
void viraresquerda(int angulo) {
  delay(100);
  motor1.run(FORWARD);
  motor2.run(RELEASE);
  motor1.setSpeed(200);
  motor2.setSpeed(0);
  delay(angulo * velang);
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  motor1.setSpeed(0);
  motor2.setSpeed(0);
}

// função para virar a direita
void virardireita(int angulo) {
  delay(100);
  motor1.run(RELEASE);
  motor2.run(FORWARD);
  motor1.setSpeed(0);
  motor2.setSpeed(200);
  delay(angulo * velang);
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  motor1.setSpeed(0);
  motor2.setSpeed(0);
}

// função para dar meia volta
void meiavolta() {
  delay(100);
  int aux = round(random(0, 10)); // definir pra que lado virar na meia volta
  if (aux <= 5) {
    viraresquerda(170); // vira pela esquerda em 180 graus
  }
  else {
    virardireita(160); // vira pela esquerda em 180 graus
  }
}

// função de interrupção após o void loop. Esta função irá ser lida a cada novo ciclo
//void serialEvent() {
//  while (Serial.available()) {
//    // pega um byte novo
//    char inChar = (char)Serial.read();
//    //char inChar = (char)Serial.read() - '0';
//    // adiciona a inputString
//    inputString += inChar;
//    // se o caractere for algo em comparação, seta a flag que será utilizada pelo loop principal
//    if (inChar == 'l') {
//      left = true;
//      stringComplete = true;  
//    }
//    if (inChar == 'r'){
//      right = true;
//      stringComplete = true;
//    } 
//    if (inChar == 'c'){
//      center = true;
//      stringComplete = true; 
//    } 
//    if (inChar == 'a'){
//      ans = true;
//      stringComplete = true;  
//    } 
//    if (inChar == 'f'){
//      front = true;
//      stringComplete = true;  
//    } 
//  }
//}

int flag = 0;
char inChar;

void establishContact() {
  if (Serial.available() <= 0 && flag == 0) {
    Serial.write('t');
    flag = 1;
    //delay(300);
  }
}

char receiveContact(){
  //char inChar;
  inChar = 'z';
  //  while(1){
  if (flag == 1)
  {
    inChar  = (char)Serial.read();    
    if(inChar == 'a'){
      flag = 0;
      return inChar;
    } 
    else if(inChar == 'r'){
      flag = 0;
      return inChar;
    } 
    else if(inChar == 'l'){
      flag = 0;
      return inChar;
    } 
    else if(inChar == 'c'){
      flag = 0;
      return inChar;
    } 
    else if(inChar == 'f'){
      flag = 0;
      return inChar;
    }
    //   delay(1);
//    else
  //  {
      //Serial.print(inChar);
    //  inChar = '0';
      return inChar;
    //}
  }     
}


