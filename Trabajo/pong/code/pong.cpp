// El comando para compilar es, con gcc >= 7:
//
// $> g++-9 -O2 -std=c++17 pong.cpp -o pong -lsfml-graphics -lsfml-window -lsfml-system
//
// Hace falta instalar SFML:
//
// sudo apt-get install libsfml-dev

#include <iostream>
#include <vector>
#include <algorithm>
#include <stdlib.h>
#include <unistd.h>

#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>
#include <SFML/Window.hpp>


using namespace std;

static const int NCOL=69;
static const int NROW=39;

static const sf::Color BACK(255, 255, 250);
static const sf::Color BALL(255, 30, 30);

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
		pair<int,int> position;
		// Para modificar la trayectoria
		int mod_x, mod_y;
	public:
		Ball(int x, int y){
			position.first=x;
			position.second=y;
			
			// Dirección
			mod_x=-1;	// Izquierda
			mod_y=0;	// -1 Arriba, 1 Abajo
		}
		
		int getX(){
			return position.first;
		}
		
		int getY(){
			return position.second;
		}
		
		auto& getPos(){
			return position;
		}
		
		void move(){
			position.first=position.first+mod_x;
			position.second=(position.second+mod_y+NROW)%NROW;
		}
		
		void setMod(int x, int y){
			mod_x=x;
			mod_y=y;
		}
		
		void reset(){
			position.first=NCOL/2;
			position.second=NROW/2;
			mod_x=-1;
			mod_y=0;
		}
		
		bool goal(){
			return (position.first==0 || position.first==NCOL-1); 
		}
};




class DrawablePong : public sf::Drawable
{
public:
    DrawablePong(Player* a_ptr,Player* b_ptr, Ball* ball_ptr)
        : m_a_ptr{a_ptr}, m_b_ptr{b_ptr}, m_ball_ptr{ball_ptr}
    {}
private:
    void draw(sf::RenderTarget& target, sf::RenderStates states) const override
    {
        // Draw the background
        target.draw(
            [&]()
            {
            	/*sf::Vector2f nose=target.getView().getSize();
            	nose.x-=30;
            	nose.y-=30;
                sf::RectangleShape background(nose);
                cout << background.getSize().x << " " << background.getSize().y << endl;
                */
                sf::RectangleShape background{target.getView().getSize()};
                background.setFillColor(BACK);
                return background;
            }(),
            states
        );

        static sf::RectangleShape square
        {
            sf::Vector2f
            {
                static_cast<float>(target.getView().getSize().x / NCOL),
                static_cast<float>(target.getView().getSize().y / NROW)
            }
        };
        square.setFillColor(sf::Color::Green);
        square.setOutlineColor(sf::Color{200, 200, 200});
        square.setOutlineThickness(1);

        for (auto [x, y] : m_a_ptr->getPos())
        {
            square.setPosition(x * square.getSize().x, y * square.getSize().y);
            target.draw(square, states);
        }
        
        for (auto [x, y] : m_b_ptr->getPos())
        {
            square.setPosition(x * square.getSize().x, y * square.getSize().y);
            target.draw(square, states);
        }
        

        //square.setFillColor(sf::Color::Red);
        square.setFillColor(BALL);
        square.setPosition
        (
            m_ball_ptr->getPos().first * square.getSize().x,
            m_ball_ptr->getPos().second * square.getSize().y
        );

        target.draw(square, states);
        
        sf::RectangleShape line(sf::Vector2f(target.getView().getSize().x, 5));
        line.setFillColor(sf::Color{255,0,0});
        target.draw(line, states);
        
        line.setPosition(0,target.getView().getSize().y-5);
        target.draw(line, states);
        
    }

    Player* m_a_ptr = nullptr;
    Player* m_b_ptr = nullptr;
    Ball* m_ball_ptr = nullptr;
};


void increaseSpeed(sf::Time &period)
{
    if (period.asMilliseconds() > 1)
        period -= sf::milliseconds(1);
}

void decreaseSpeed(sf::Time &period)
{
    if (period.asMilliseconds() < 500)
        period += sf::milliseconds(1);
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

void update(Player &a, Player &b, Ball &p,int i){
	if(i==0){	
		int random_movement=rand()%100;
		
		if(random_movement<65)		b.moveUp();//movePlayer(b,true);
		if(random_movement>65)		b.moveDown();//movePlayer(b,false);
	}	

	p.move();
	rebotar(a,b,p); // Para rebotar la pelota contra las raquetas
}


int main(){
		
	sf::RenderWindow window(sf::VideoMode(NCOL*10*3/2, NROW*10*3/2), "Pong (not running)");

	// Inicializar jugadores
	// Si se cambia la longitud de la raqueta (7) la función rebotar no va a funcionar bien
	Player a(3,NROW/2-3,7);
	Player b(NCOL-4,NROW/2-3,7);
	
	// Inicializar pelota (en medio del tablero)
	Ball p(NCOL/2, NROW/2);
    DrawablePong grid(&a, &b, &p);

    bool running = false;
    sf::Clock timer;
    sf::Time period = sf::milliseconds(70);

	// Para los movimientos aleatorios
	int iter=0;
	int velocidad_ia=4;

    while (window.isOpen())
    {
        sf::Event event{};

        while (window.pollEvent(event))
        {
            switch (event.type)
            {
                case sf::Event::Closed:
                    window.close();
                    break;
                case sf::Event::KeyPressed:
                    switch (event.key.code)
                    {
                        case sf::Keyboard::Up:
                            increaseSpeed(period);
                            break;
                        case sf::Keyboard::Down:
                            decreaseSpeed(period);
                            break;
                        default:
                            break;
                    }
                    break;
                case sf::Event::KeyReleased:
                    switch (event.key.code)
                    {
                        case sf::Keyboard::Q:
                        case sf::Keyboard::Escape:
                            window.close();
                            break;
                        case sf::Keyboard::Space:
                            running = !running;

                            if (running)
                                window.setTitle("Pong (running)");
                            else
                                window.setTitle("Pong (not running)");

                            break;
                        case sf::Keyboard::W:
                            a.moveUp();
                            break;
                        case sf::Keyboard::S:
                            a.moveDown();
                            break;
                        default:
                            break;
                    }

                    break;
                default:
                    break;
            }
        }

        if (running && timer.getElapsedTime() > period)
        {
            update(a,b,p,iter);
            timer.restart();
        }
        
        iter++;
		iter=iter%velocidad_ia;
		
		if(p.goal()){
			p.reset();
			running=false;
			window.setTitle("Pong (not running)");
		}    	
			    	
        window.clear();
        window.draw(grid);
        window.display();
    }
	
}
