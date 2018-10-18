#include <iostream>
#include <wiringPi.h>
#include <mcp3004.h>
#include <thread>
#include <chrono>

#define BASE 100
#define SPI_CHAN 0

using namespace std;

int main()
{
    wiringPiSetupGpio();
    mcp3004Setup(BASE, SPI_CHAN);

    int x;
    float V;

    while(true){
        x = analogRead(BASE);
        V = float(x) / 1023 * 3.323;
        cout << x << '\n';
        cout << V << '\n' << '\n';
        this_thread::sleep_for(chrono::milliseconds(1000));
    }

    return 0;
}
