/*
Para compilar (en linux):
	g++ pong.cpp -o pong -std=gnu++17
Para ejecutar:
	./pong
Para mover la raqueta, "w" arriba, "s" abajo, y pulsar INTRO.
*/

#include <iostream>
#include <vector>
#include <algorithm>
#include <stdlib.h>
#include <unistd.h>

using namespace std;

static const int NCOL=79;
static const int NROW=19;


class Player{
	private:
		int longitud;
		vector< pair<int,int> > positions;
	public:
		Player(int x, int y, int len){
			for(int i=0;i<len;i++){
				positions.push_back({x,(y+i)%NROW});
			}
			longitud=len;
		}
		
		int getX(){
			return positions.front().first;
		}
		
		vector<int> getY(){
			vector<int> tmp;
			for(int i=0; i<positions.size(); i++)	tmp.push_back(positions[i].second);
			return tmp;
		}
		
		auto& getPos(){
			return positions;
		}
		
		void move(bool up){
			if(up)
				for(int i=0; i<longitud;i++)
					positions[i].second=(positions[i].second-1+NROW)%NROW;
			else
				for(int i=0; i<longitud;i++)
					positions[i].second=(positions[i].second+1)%NROW;
		}
		
		void moveUp(){
			for(int i=0; i<longitud;i++)
				positions[i].second=(positions[i].second-1+NROW)%NROW;		
		}
		
		void moveDown(){
			for(int i=0; i<longitud;i++)
				positions[i].second=(positions[i].second+1)%NROW;
		}
};

class Ball{
	private:
		int pos_x;
		int pos_y;
		// Para modificar la trayectoria
		int mod_x, mod_y;
	public:
		Ball(int x, int y){
			pos_x=x;
			pos_y=y;
			
			// Dirección
			mod_x=-1;	// Izquierda
			mod_y=0;	// -1 Arriba, 1 Abajo
		}
		
		int getX(){
			return pos_x;
		}
		
		int getY(){
			return pos_y;
		}
		
		void move(){
			pos_x=pos_x+mod_x;
			pos_y=(pos_y+mod_y+NROW)%NROW;
		}
		
		void setMod(int x, int y){
			mod_x=x;
			mod_y=y;
		}
		
		void reset(){
			pos_x=NCOL/2;
			pos_y=NROW/2;
			mod_x=-1;
			mod_y=0;
		}
};





void print(Player a, Player b, Ball p){
	int pos_X_a=a.getX();
	int pos_X_b=b.getX();
	vector<int> pos_Y_a=a.getY();
	vector<int> pos_Y_b=b.getY();
	
	int pos_X_p=p.getX();
	int pos_Y_p=p.getY();
	
	cout << "Pelota: " <<pos_X_p<<", "<<pos_Y_p<<"     ";
	
	// Posición de la raqueta que controlamos
	for(int i=0; i<pos_Y_a.size(); i++){
		cout << pos_Y_a[i]<< "; ";
	}
	cout << endl;
	
	// Borde Superior
	for(int i=0;i<NCOL;i++){
		cout << "-";
	}
	cout << endl;
	
	// Tablero
	for(int i=0; i<NROW; i++){
		for(int j=0; j<NCOL; j++){
		
			if(j==pos_X_p && i==pos_Y_p){
				cout << "o";
			}else if(j==pos_X_a && find(pos_Y_a.begin(), pos_Y_a.end(), i) != pos_Y_a.end()){
				cout << "#";
			}else if(j==pos_X_b && find(pos_Y_b.begin(), pos_Y_b.end(), i) != pos_Y_b.end()){
				cout << "#";
			}else{
				cout << " ";
			}
		}
		cout << endl;
	}
	
	// Borde Inferior
	for(int i=0;i<NCOL;i++){
		cout << "-";
	}
	cout << endl;
	
}


void movePlayer(Player &a, bool up){
	a.move(up);	
}

void moveBall(Ball &b){
	b.move();
}


void input(Player &a, Player &b, Ball &p,int i){	
	char input;
	cin >>input;
	
	if(input=='w')					a.moveUp();//movePlayer(a,true);
	else if(input=='s')				a.moveDown();//movePlayer(a,false);
	
	if(i==0){	
		int random_movement=rand()%100;
		
		if(random_movement<65)			b.moveUp();//movePlayer(b,true);
		if(random_movement>65)			b.moveDown();//movePlayer(b,false);
	}	
	moveBall(p);
}


void rebotar(Player a, Player b, Ball &p){
	// Cuando da en las esquinas sale en diagonal
	// Cuando da en el centro sale en línea recta

	if(p.getX()-1==a.getX()){
		vector<int> raqueta=a.getY();
		for(int i=0; i<raqueta.size(); i++){
			if(raqueta[i]==p.getY()){
				if(i==0 || i==1)			p.setMod(1,-1);
				if(i==2 || i==3 || i==4)	p.setMod(1,0);
				if(i==5 || i==6)			p.setMod(1,1);
				break;
			}
		}
	}
	
	if(p.getX()+1==b.getX()){
		vector<int> raqueta=b.getY();
		for(int i=0; i<raqueta.size(); i++){
			if(raqueta[i]==p.getY()){
				if(i==0 || i==1)			p.setMod(-1,-1);
				if(i==2 || i==3 || i==4)	p.setMod(-1,0);
				if(i==5 || i==6)			p.setMod(-1,1);
				
				break;
			}
		}
	}
}



int main(){
	
	// Inicializar jugadores
	// Si se cambia la longitud de la raqueta (7) la función rebotar no va a funcionar bien
	Player a(3,6,7);
	Player b(NCOL-4,6,7);
	
	// Inicializar pelota (en medio del tablero)
	Ball p(NCOL/2, NROW/2);
	
	int iter=0;
	int velocidad_ia=4;
	while(true){
		do{
			print(a,b,p); // Dibujamos el mapa
		
		
			// Para poder manejar la raqueta quitar el comentario en el cin de esta función
			input(a,b,p,iter); // Para mover los objetos
				
			rebotar(a,b,p); // Para rebotar la pelota contra las raquetas
		
			usleep(50000);
			iter++;
			iter=iter%velocidad_ia;
		
		}while(p.getX()!=0 && p.getX()!=NCOL-1); // POSICIÓN DE GOL
		p.reset();
		print(a,b,p);
		usleep(500000);
	}
	
	cout << endl;
	
	return 0;
}
