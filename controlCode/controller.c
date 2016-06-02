
#include <avr/io.h>
#include <stdio.h>
#include <dynamixel.h>
#include <serial.h>
#include <math.h>
#include <stdlib.h>

#define pi 3.14
#define a  0.4974189//0.523599//0.46635199//  to be calibrated for each robot Note: All angles are in radians
#define b  2.6441739//2.61799//2.67524075//
#define c  4.71239

void PrintCommStatus(int CommStatus); // For Status Checking 
void PrintErrorCode(void);


int main(void)
{
    
while (1) 
       {	
		
		float x;           	// X,Y values to be acquired from the remote control
        float y;
		float r1;         // r1 for getting the rotational values
		int rot;          // rot for rotating the robot
		float mag, ta; 		
		int v1,v2,v3;
		int vmax =464;      // compensation for 12v battery power supply; refer the MX 28 website for move info
		printf("\nx=");
		scanf("%f", x); 
		printf("\ny=");
		scanf("%f", y); 

		ta= atan2(y, x);		//Converting to polar coordinates
      	mag= sqrt((x*x)+(y*y));	
		mag= ((mag>1)?1:mag);
		mag= mag*vmax;
		ta= ta-1.5708;

		
       printf( "Mag=%f   Theta=%f\n", mag, ta );
	
       v1= mag*cos(a-ta);                              // getting velocities of the each motors using Kinematic Equation
				
	   v2= mag*cos(b-ta);
				
	   v3= mag*cos(c-ta);
	   
	   	
	
	   printf( "v1=%d   v2=%d  v3=%d\n", v1, v2, v3 );
	
        serial_initialize(57600);						//Initializing dynamixels
	dxl_initialize( 0, DEFAULT_BAUDNUM ); // Not using device index
	sei();	// Interrupt Enable


		//wheel mode initialization					// Assigning dynamixels to wheel mode for three wheels Cw limit = ccw limit = 0
		dxl_write_word( 1, 6, 0 ); 
		dxl_write_word( 1, 8, 0 );
		
		dxl_write_word( 2, 6, 0 );
		dxl_write_word( 2, 8, 0 );
		
		dxl_write_word( 3, 6, 0 );
		dxl_write_word( 3, 8, 0 );
		
		if (v1<0)							//Checking whether CW or CCW rotation
		{
			v1= fabsf(v1);
			
			dxl_write_word( 1, 32, v1);			 	//Writing to Dynamixel ID1
		} 
		else
		{
			
		    v1= v1+1024;
			dxl_write_word( 1,32, v1 );
		}
		
		if (v2<0)
		{
			v2= fabsf(v2);
			
			dxl_write_word( 2, 32, v2);
		}
		else
		{
			
			v2= v2+1024;
			dxl_write_word( 2,32, v2 );
		}
		
		if (v3<0)
		{
			v3= fabsf(v3);
			
			dxl_write_word( 3, 32, v3);
		}
		else
		{
			
			v3= v3+1024;
			dxl_write_word( 3,32, v3 );
		}
             
		if(r1>0)
		{
			rot= r1*vmax;
			rot= 1024+ rot;
			dxl_write_word( 1, 32, rot);
			dxl_write_word( 2, 32, rot);
			dxl_write_word( 3, 32, rot);
		}
		else|
		{
			r1= fabsf(r1);
			rot= r1*vmax;
			dxl_write_word( 1, 32, rot);
			dxl_write_word( 2, 32, rot);
			dxl_write_word( 3, 32, rot);
			
		}
		

			 CommStatus = dxl_get_result();
		if( CommStatus == COMM_RXSUCCESS )
		PrintErrorCode();
		else
		PrintCommStatus(CommStatus);
   
   
 }

}

void PrintCommStatus(int CommStatus)
{
	switch(CommStatus)
	{
		case COMM_TXFAIL:
		printf("COMM_TXFAIL: Failed transmit instruction packet!\n");
		break;

		case COMM_TXERROR:
		printf("COMM_TXERROR: Incorrect instruction packet!\n");
		break;

		case COMM_RXFAIL:
		printf("COMM_RXFAIL: Failed get status packet from device!\n");
		break;

		case COMM_RXWAITING:
		printf("COMM_RXWAITING: Now recieving status packet!\n");
		break;

		case COMM_RXTIMEOUT:
		printf("COMM_RXTIMEOUT: There is no status packet!\n");
		break;

		case COMM_RXCORRUPT:
		printf("COMM_RXCORRUPT: Incorrect status packet!\n");
		break;

		default:
		printf("This is unknown error code!\n");
		break;
	}
}

// Print error bit of status packet
void PrintErrorCode()
{
	if(dxl_get_rxpacket_error(ERRBIT_VOLTAGE) == 1)
	printf("Input voltage error!\n");

	if(dxl_get_rxpacket_error(ERRBIT_ANGLE) == 1)
	printf("Angle limit error!\n");

	if(dxl_get_rxpacket_error(ERRBIT_OVERHEAT) == 1)
	printf("Overheat error!\n");

	if(dxl_get_rxpacket_error(ERRBIT_RANGE) == 1)
	printf("Out of range error!\n");

	if(dxl_get_rxpacket_error(ERRBIT_CHECKSUM) == 1)
	printf("Checksum error!\n");

	if(dxl_get_rxpacket_error(ERRBIT_OVERLOAD) == 1)
	printf("Overload error!\n");

	if(dxl_get_rxpacket_error(ERRBIT_INSTRUCTION) == 1)
	printf("Instruction code error!\n");
}
