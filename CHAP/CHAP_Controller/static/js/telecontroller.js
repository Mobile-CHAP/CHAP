function runController(hostName,devMode) {
	
	var DEVELOPER_MODE = devMode == "True" ? true : false;
	console.log(devMode);
	//Create Variables and listeners
	var canvas = document.getElementById("canvas");
	var canvasGrip = document.getElementById("gripperControls");
	
	var ctx = canvas.getContext("2d");
	var ctxGrip = canvasGrip.getContext("2d");
	
	var gripControlBox = canvasGrip.getBoundingClientRect();
	
	var joystickOn = false;
	var sliderOn = false;
	var pinchOn = false;
	var hasTouchScreen = false;
	var checkedDirection = false;
	
	var gripperControlOn = false;

	//Controls
	var g_wrist = {
		width: 0,
		x: 0,
		value: 0
	}
	var g_knuckle = {
		width: 0,
		x: 0,
		value: 0.5
	}
	var g_finger = {
		width: 0,
		x: 0,
		value: 0
	}
	var gripperOffset = 30;
	var gripperSlideHeight = 30;
	
	
	var joystick = {
		center: null,
		stick: null
	};
	var slider = {
		main: null,
		tab: null,
		isVertical: true
	};
	var pinch = {
		touches: [],
		distance: 0
	};
	var colours = {
		center_mouse: "rgb(150,150,150)",
		stick_mouse: "rgb(50,50,50)",
		center_touch: "rgb(0,205,240)",
		stick_touch: "rgb(46,255,255)"
	}	

	//Get hostname from Flask
	//var hostName = "{{ serverIPAddress }}";
	var socketController = null;
	
	window.onerror = function(message, url, lineNumber) {  
	  socketController.send("[ERROR]//" + message + " URL:" + url + " LINE:" + lineNumber);
	};  

	canvas.addEventListener( 'touchstart', onTouchStart, false );
	canvas.addEventListener( 'touchmove', onTouchMove, false );
	canvas.addEventListener( 'touchend', onTouchEnd, false );
	canvas.addEventListener( 'touchcancel', onTouchCancel, false);

	canvas.addEventListener( 'mousedown', onTouchStart, false );
	canvas.addEventListener( 'mousemove', onTouchMove, false );
	canvas.addEventListener( 'mouseup', onTouchEnd, false );
	canvas.addEventListener( 'mouseleave', onTouchCancel, false);
	canvas.addEventListener( 'mouseout', onTouchCancel, false);
	
	canvasGrip.addEventListener( 'touchstart', onTouchGripStart, false );
	canvasGrip.addEventListener( 'touchmove', onTouchGripMove, false );
	canvasGrip.addEventListener( 'touchend', onTouchGripEnd, false );
	canvasGrip.addEventListener( 'touchcancel', onTouchCancel, false);

	canvasGrip.addEventListener( 'mousedown', onTouchGripStart, false );
	canvasGrip.addEventListener( 'mousemove', onTouchGripMove, false );
	canvasGrip.addEventListener( 'mouseup', onTouchGripEnd, false );
	canvasGrip.addEventListener( 'mouseleave', onTouchCancel, false);
	canvasGrip.addEventListener( 'mouseout', onTouchCancel, false);

	//Prepare page
	document.oncontextmenu = function() {return false;};
	window.addEventListener('resize', resizeCanvas, false);
	resizeCanvas();

	function startSocket() {
		socketController = new WebSocket("ws://"+hostName+":9001");
		socketController.onopen = function(){
			console.log('Connected to dynamixel socket',socketController.url);
			document.getElementById("errorMessage").style.display = "none";
		};
		socketController.onclose = function(){
			console.log('Disconnected from dynamixel socket',socketController.url);
			document.getElementById("errorMessage").style.display = "block";
			checkSocket();
		};
	}
	function checkSocket(){
		if (!socketController || socketController.readyState == WebSocket.CLOSED){
			document.getElementById("errorMessage").style.display = "block";
			startSocket();
		}
	}
	
	if(!DEVELOPER_MODE){
		startSocket();
		setInterval(checkSocket,5000);
	}

	function resizeCanvas (event) {
		canvas.width = document.body.clientWidth;
		canvas.height = document.body.clientHeight;		
		
		canvasGrip.width = document.body.clientWidth*0.3;
		canvasGrip.height = document.body.clientHeight*0.3;	

		gripControlBox = canvasGrip.getBoundingClientRect();
		gripperOffset = canvasGrip.width * 0.15;
		g_wrist.width = g_knuckle.width = g_finger.width = (canvasGrip.width/3)-gripperOffset;
		
		g_wrist.x = gripperOffset/2
		g_knuckle.x = (g_wrist.x + g_wrist.width)+gripperOffset;
		g_finger.x = (g_knuckle.x + g_knuckle.width)+gripperOffset;
		gripperSlideHeight = canvasGrip.height*0.2;
		
		reDraw();
	};
		
	function onTouchStart(event){
		event.preventDefault();
		gripperControlOn = false;

		if(event.touches){
			hasTouchScreen = true;
			for(var touch of event.touches){
				if(touch.pageX > canvas.width/2){
					joystick.center = touch;
					joystick.stick = touch;
					joystickOn = true;
					
					pinch.touches.push(touch);
					if(pinch.touches.length >= 2){
						joystickOn = false;
						pinchOn = true;
					}
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

				sendToSocket("leftSliderVert",0,(currentEvent.pageY-slider.main.pageY));
			}
		} else {
			if(currentEvent.pageX <= slider.main.pageX + 100 &&
				currentEvent.pageX >= slider.main.pageX - 100){
				slider.tab = currentEvent;

				sendToSocket("leftSliderHorz",(currentEvent.pageX-slider.main.pageX),0);
			}
		}

		reDraw();
	}

	function joystickUpdate(currentEvent){
		var distance = getDistance(joystick.center,currentEvent);

		if(distance.dist <= 100){
			joystick.stick = currentEvent;

			sendToSocketFlip("rightJoystick",distance.x,distance.y);
		}
		
		reDraw();
	}

	function pinchUpdate(){
		if(pinch.touches >= 2){
			pinch.distance = getDistance(pinch.touches[0],pinch.touches[1]);
			sendToSocketFlip("rightPinch",pinch.distance,0);
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
		} else if (pinchOn){
			pinch.touches = [];
			for(var touch of event.touches){
				if(touch.pageX > canvas.width/2){
					if(pinch.touches.length < 2){
						pinch.touches.push(touch);
					}
				}
			}
			pinchUpdate();
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
			pinch.touches = [];
			ctx.clearRect(0, 0, canvas.width, canvas.height);
			sendToSocketFlip("rightJoystick",0,0);
		}
		if(sliderOn){
			sliderOn = false;
			checkedDirection = false;
			ctx.clearRect(0, 0, canvas.width, canvas.height);
			if(slider.isVertical){
				sendToSocket("leftSliderVert",0,0)
			} else {
				sendToSocketFlip("rightJoystick",0,0);
			}
		}
		if(pinchOn){
			pinchOn = false;
			pinch.touches = [];
			ctx.clearRect(0, 0, canvas.width, canvas.height);
			sendToSocketFlip("rightPinch",0,0);
		}
	}
	
	function onTouchGripStart(event){
		event.preventDefault();
		gripperControlOn = true;
		joystickOn = false;
		sliderOn = false;
		pinchOn = false;
		
		if(event.touches){
			hasTouchScreen = true;
			updateGripper(event.touches[0]);
		} else{
			updateGripper(event);
		}
	}
	function onTouchGripMove(event){
		event.preventDefault();
		joystickOn = false;
		sliderOn = false;
		pinchOn = false;
		
		if(hasTouchScreen){
			updateGripper(event.touches[0]);
		} else{
			updateGripper(event);
		}

	}
	function onTouchGripEnd(event){
		gripperControlOn = false;
		
		resetKnuckle();
		//ctxGrip.clearRect(0, 0, canvasGrip.width, canvasGrip.height);
	}
	
	function onTouchCancel(event){
		gripperControlOn = false;
		joystickOn = false;
		sliderOn = false;
		pinchOn = false;
		resetKnuckle();
		sendToSocket("leftSliderVert",0,0);
		sendToSocketFlip("rightJoystick",0,0);
	}
	
	function resetKnuckle()
	{
		g_knuckle.value = 0.5;
		sendToSocketGripper("gripper_knuckle",0);
		reDraw();
	}
	
	function updateGripper(e){
		
		if(gripperControlOn){
			var currentX = null;
			var newValue = 0;
			
			newValue = (e.pageY-gripControlBox.top)/canvasGrip.height;
			currentX = e.pageX-gripControlBox.left;
			
			if (newValue > 1){
				newValue = 1;
			} else if (newValue < 0){
				newValue = 0;
			}
			
			//socketController.send("[ERROR]//Value: " + newValue);

			if (currentX > g_wrist.x && currentX < g_wrist.x + g_wrist.width){
				g_wrist.value = newValue;
				sendToSocketGripper("gripper_wrist",1-newValue);
			} 
			else if (currentX > g_knuckle.x && currentX < g_knuckle.x + g_knuckle.width){
				
				g_knuckle.value = newValue;
				sendToSocketGripper("gripper_knuckle",0.5-newValue);
				
			} 
			else if (currentX > g_finger.x && currentX < g_finger.x + g_finger.width){
				g_finger.value = newValue;
				sendToSocketGripper("gripper_finger",1-newValue);
			}
			
			reDraw();
		}
	}
	
	function reDraw(){
		ctx.clearRect(0, 0, canvas.width, canvas.height);
		ctxGrip.clearRect(0, 0, canvasGrip.width, canvasGrip.height);
		ctxGrip.setLineDash([])
		
		if(joystickOn){
			ctx.strokeStyle = hasTouchScreen ? colours.center_touch : colours.center_mouse;
			ctx.lineWidth = 2;
			ctx.beginPath();
			ctx.arc(joystick.center.pageX-10,joystick.center.pageY+40,80,0,2*Math.PI);
			ctx.stroke();
			
			ctx.strokeStyle = hasTouchScreen ? colours.stick_touch : colours.stick_mouse;
			ctx.beginPath();
			ctx.arc(joystick.stick.pageX-10,joystick.stick.pageY+40,40,0,2*Math.PI);
			ctx.stroke();
		}

		if(pinchOn){
			ctx.strokeStyle = hasTouchScreen ? colours.stick_touch : colours.stick_mouse;
			
			ctx.beginPath();
			ctx.moveTo(pinch.touches[0].pageX-5,pinch.touches[0].pageY-40);
			ctx.lineTo(pinch.touches[1].pageX-5,pinch.touches[1].pageY-40);
			ctx.stroke();
			
			for(var touch of pinch.touches){
				ctx.beginPath();
				ctx.arc(touch.pageX-10,touch.pageY-40,40,0,2*Math.PI);
				ctx.stroke();
			}
		}

		if(sliderOn){
			ctx.strokeStyle = hasTouchScreen ? colours.center_touch : colours.center_mouse;
			ctx.lineWidth = 2;
			ctx.beginPath();
			if(slider.isVertical){
				ctx.rect(slider.main.pageX-25,slider.main.pageY-120,50,200);
			} else {
				ctx.rect(slider.main.pageX-100,slider.main.pageY-25,200,50);
			}
			ctx.stroke();
			
			ctx.strokeStyle = hasTouchScreen ? colours.stick_touch : colours.stick_mouse;
			ctx.beginPath();
			if(slider.isVertical){
				ctx.rect(slider.main.pageX-40,slider.tab.pageY-30,80,20);
			} else {
				ctx.rect(slider.tab.pageX-10,slider.main.pageY-40,20,80);
			}
			ctx.stroke();
		}

		//Gripper Controls
		ctxGrip.strokeStyle = hasTouchScreen ? "rgb(255,255,255)" : "rgb(0,0,0)";
		ctxGrip.fillStyle = hasTouchScreen ? "rgb(255,255,255)" : "rgb(0,0,0)";
		ctxGrip.beginPath();
			ctxGrip.font = "0.75em Arial";
			ctxGrip.textAlign = "center";
			ctxGrip.fillText("Hand",g_knuckle.x+(g_knuckle.width/2),15);
			ctxGrip.font = "0.5em Arial";
			ctxGrip.fillText("Open",g_knuckle.x+(g_knuckle.width/2),30);
			ctxGrip.fillText("Close",g_knuckle.x+(g_knuckle.width/2),canvasGrip.height-15);
			
			ctxGrip.font = "0.75em Arial";
			ctxGrip.textAlign = "center";
			ctxGrip.fillText("Finger",g_finger.x+(g_finger.width/2),15);
			ctxGrip.font = "0.5em Arial";
			ctxGrip.fillText("Open",g_finger.x+(g_finger.width/2),30);
			ctxGrip.fillText("Close",g_finger.x+(g_finger.width/2),canvasGrip.height-15);
			
			ctxGrip.font = "0.5em Arial";
			ctxGrip.textAlign = "center";
			ctxGrip.fillText("Rotate CW",g_wrist.x+(g_wrist.width/2),15);
			ctxGrip.fillText("Rotate CCW",g_wrist.x+(g_wrist.width/2),canvasGrip.height-15);
		ctxGrip.stroke();
		
		ctxGrip.strokeStyle = hasTouchScreen ? colours.center_touch : colours.center_mouse;
		ctxGrip.lineWidth = 2;
		ctxGrip.beginPath();
			ctxGrip.rect(g_finger.x,0,g_finger.width,canvasGrip.height);
			ctxGrip.rect(g_knuckle.x,0,g_knuckle.width,canvasGrip.height);
			ctxGrip.rect(g_wrist.x,0,g_wrist.width,canvasGrip.height);
		ctxGrip.stroke();
		

		ctxGrip.beginPath();
			ctxGrip.moveTo(g_knuckle.x+(g_knuckle.width/2),(canvasGrip.height*0.5)-gripperSlideHeight/2);
			ctxGrip.lineTo(g_knuckle.x+(g_knuckle.width/2),(canvasGrip.height*g_knuckle.value)-gripperSlideHeight/2);
		ctxGrip.stroke();
		
		ctxGrip.setLineDash([])
		ctxGrip.fillStyle = hasTouchScreen ? colours.stick_touch : colours.stick_mouse;
		ctxGrip.beginPath();
			ctxGrip.fillRect(g_finger.x-5,(canvasGrip.height*g_finger.value)-gripperSlideHeight/2,g_finger.width+10,gripperSlideHeight);
			ctxGrip.fillRect(g_knuckle.x-5,(canvasGrip.height*g_knuckle.value)-gripperSlideHeight/2,g_knuckle.width+10,gripperSlideHeight);
			ctxGrip.fillRect(g_wrist.x-5,(canvasGrip.height*g_wrist.value)-gripperSlideHeight/2,g_wrist.width+10,gripperSlideHeight);
		ctxGrip.stroke();
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
	
	function getDistance(original,event){
		var difX = event.pageX-original.pageX;
		var difY = original.pageY-event.pageY;
		
		var hyp = Math.sqrt(Math.pow(difX, 2)+Math.pow(difY, 2));
		return {dist: hyp,x:difX,y:difY};
	}

	function sendToSocketFlip(controlName,x,y)
	{
		x = x * -1
		y = y * -1
		var xF = Number((x/100).toFixed(3));
		var yF = Number((y/100).toFixed(3));
		var result = "[BODY]"+controlName+","+xF+","+yF;

		if(!DEVELOPER_MODE){
			socketController.send(result);
		}
		
	}
	
	function sendToSocket(controlName,x,y)
	{
		var xF = Number((x/100).toFixed(3));
		var yF = Number((y/100).toFixed(3));
		var result = "[BODY]"+controlName+","+xF+","+yF;

		if(!DEVELOPER_MODE){
			socketController.send(result);
		}
		
	}
	
	function sendToSocketGripper(controlName,value)
	{
		var valueF = Number(value).toFixed(3);
		var result = "[HAND]"+controlName+","+valueF;

		if(!DEVELOPER_MODE){
			socketController.send(result);
		}
		
	}
}