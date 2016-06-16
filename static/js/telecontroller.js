function runController(hostName) {

	//Create Variables and listeners
	var canvas = document.getElementById("canvas");
	var ctx = canvas.getContext("2d");
	var joystickOn = false;
	var sliderOn = false;
	var hasTouchScreen = false;
	var checkedDirection = false;

	//Controls
	var joystick = {
		center: null,
		stick: null
	};
	var slider = {
		main: null,
		tab: null,
		isVertical: true
	};
	var colours = {
		center_mouse: "rgb(150,150,150)",
		stick_mouse: "rgb(50,50,50)",
		center_touch: "rgb(0,205,240)",
		stick_touch: "rgb(46,255,255)"
	}	

	//Get hostname from Flask
	//var hostName = "{{ serverIPAddress }}";
	console.log(hostName);
	var socketController = new WebSocket("ws://"+hostName+":9001");

	canvas.addEventListener( 'touchstart', onTouchStart, false );
	canvas.addEventListener( 'touchmove', onTouchMove, false );
	canvas.addEventListener( 'touchend', onTouchEnd, false );

	canvas.addEventListener( 'mousedown', onTouchStart, false );
	canvas.addEventListener( 'mousemove', onTouchMove, false );
	canvas.addEventListener( 'mouseup', onTouchEnd, false );

	//Prepare page
	document.oncontextmenu = function() {return false;};
	window.addEventListener('resize', resizeCanvas, false);
	resizeCanvas();

	function resizeCanvas (event) {
		canvas.width = document.body.clientWidth;
		canvas.height = document.body.clientHeight;
		reDraw();
	};
		
	function onTouchStart(event){
		event.preventDefault();

		if(event.touches){
			hasTouchScreen = true;

			for(var touch of event.touches){
				if(touch.pageX > canvas.width/2){
					joystick.center = touch;
					joystick.stick = touch;
					joystickOn = true;
				} else {
					slider.main = touch;
					slider.tab = touch;
					sliderOn = true;
				}
			}
		} 
		else 
		{
			if(event.buttons == 1){
				joystick.center = event;
				joystick.stick = event;
				joystickOn = true;
			} else if (event.buttons == 2){
				slider.main = event;
				slider.tab = event;
				sliderOn = true;
			}
			hasTouchScreen = false;
		}

		reDraw();
	}

	function sliderUpdate(currentEvent){

		if(!checkedDirection){
			getSliderDirection(currentEvent);
		}

		if(slider.isVertical){
			if(currentEvent.pageY <= slider.main.pageY + 100 &&
				currentEvent.pageY >= slider.main.pageY - 100){
				slider.tab = currentEvent;

				sendToSocket("leftSliderVert",0,(slider.main.pageY-currentEvent.pageY));
			}
		} else {
			if(currentEvent.pageX <= slider.main.pageX + 100 &&
				currentEvent.pageX >= slider.main.pageX - 100){
				slider.tab = currentEvent;

				sendToSocket("leftSliderHorz",(slider.main.pageY-currentEvent.pageY),0);
			}
		}

		reDraw();
	}

	function joystickUpdate(currentEvent){
		var distance = getDistance(currentEvent);

		if(distance.dist <= 100){
			joystick.stick = currentEvent;

			sendToSocket("rightJoystick",distance.x,distance.y);
		}
		
		reDraw();
	}
	
	function onTouchMove(event){
		event.preventDefault();

		if(joystickOn && sliderOn){
			if(hasTouchScreen){
				for(var touch of event.touches){
					if(touch.pageX > canvas.width/2){
						joystickUpdate(touch);
					} else {
						sliderUpdate(touch);
					}
				} 
			}
		} else if(joystickOn){
			if(hasTouchScreen){
				joystickUpdate(event.touches[0]);
			} else {
				joystickUpdate(event);
			}
			
		} else if(sliderOn){
			if(hasTouchScreen){
				sliderUpdate(event.touches[0]);
			} else {
				sliderUpdate(event);
			}
		}
	}
	
	function onTouchEnd(event){
		if(joystickOn){
			joystickOn = false;
			ctx.clearRect(0, 0, canvas.width, canvas.height);
			sendToSocket("rightJoystick",0,0);
		}
		if(sliderOn){
			sliderOn = false;
			checkedDirection = false;
			ctx.clearRect(0, 0, canvas.width, canvas.height);
			sendToSocket("leftSlider",0,0);
		}
	}
	
	function reDraw(){
		ctx.clearRect(0, 0, canvas.width, canvas.height);
		var image = document.getElementById("source");
		if(joystickOn){
			ctx.strokeStyle = hasTouchScreen ? colours.center_touch : colours.center_mouse;
			ctx.lineWidth = 2;
			ctx.beginPath();
			ctx.arc(joystick.center.pageX-20,joystick.center.pageY-20,80,0,2*Math.PI);
			ctx.stroke();
			
			ctx.strokeStyle = hasTouchScreen ? colours.stick_touch : colours.stick_mouse;
			ctx.beginPath();
			ctx.arc(joystick.stick.pageX-10,joystick.stick.pageY-10,40,0,2*Math.PI);
			ctx.stroke();
		}

		if(sliderOn){
			ctx.strokeStyle = hasTouchScreen ? colours.center_touch : colours.center_mouse;
			ctx.lineWidth = 2;
			ctx.beginPath();
			if(slider.isVertical){
				ctx.rect(slider.main.pageX-25,slider.main.pageY-100,50,200);
			} else {
				ctx.rect(slider.main.pageX-100,slider.main.pageY-25,200,50);
			}
			ctx.stroke();
			
			ctx.strokeStyle = hasTouchScreen ? colours.stick_touch : colours.stick_mouse;
			ctx.beginPath();
			if(slider.isVertical){
				ctx.rect(slider.main.pageX-40,slider.tab.pageY-10,80,20);
			} else {
				ctx.rect(slider.tab.pageX-10,slider.main.pageY-40,20,80);
			}
			ctx.stroke();
		}
	}

	function getSliderDirection(currentEvent){
		var xDif = Math.abs(currentEvent.pageX - slider.main.pageX);
		var yDif = Math.abs(currentEvent.pageY - slider.main.pageY);

		if (xDif > 5 || yDif > 5){
			if(xDif < yDif){
				slider.isVertical = true;
			} else {
				slider.isVertical = false;
			}
			checkedDirection = true;
		}
	}
	
	function getDistance(event){
		var difX = joystick.center.pageX-event.pageX;
		var difY = joystick.center.pageY-event.pageY;
		
		var hyp = Math.sqrt(Math.pow(difX, 2)+Math.pow(difY, 2));
		return {dist: hyp,x:difX,y:difY};
	}

	function sendToSocket(controlName,x,y)
	{
		var xF = Number((x/100).toFixed(3));
		var yF = Number((y/100).toFixed(3));
		var result = controlName+","+xF+","+yF;
		socketController.send(result);
	}
}