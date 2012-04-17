// modified by Jeremy Parks
var metaaps={};

metaaps.nebulos=function(b){
//	this.container=b;
	var c=b.width;
	var a=b.height;
	this.canvas=b;//canvasport.createCanvas(b,c,a,{margin:"0px",padding:"0px",border:"none"});
	this.opacityvalue=0.9;
	this.notestboxes=true;
	this.stroke=true;
	this.screenportion=0.3;
	this.fillstyle={red:0,green:0,blue:0};
	this.strokestyle="rgba(0, 0, 0, 0.1)";
	this.shaded=true;
	this.multicolor=false;
	this.boxes=[];
	this.running=false;
	this.restarthandler=null;
	this.directions=["ne","se","nw","sw"];
	this.fontfamily="serif";
	this.minWordSize=3;
	this.textlist=[];
	this.symbols=[];
	this.commonwords=[];
	this.measureText=function(g,f,e,d){
		if(e){
			return{height:canvasport.measureText(d,g),width:f}
		}
		else{
			return{width:canvasport.measureText(d,g),height:f}
		}
	};
	this.findPosition=function(g,e,d,i,n){
		for(var h=0;h<150;h+=3){
			var l=this.directions[i%this.directions.length];
			var k=this.getPosition(g,l,h);
			if(n.getImageData&&this.notestboxes){
				if(canvasport.hitTest(n,k.x,(d?k.y-e.height:k.y),e.width,e.height,true)==false){
					return k
				}
			}
			else{
				var m={x:k.x,y:(d?k.y-e.height:k.y),width:e.width,height:e.height};
				for(var f=0;f<this.boxes.length;f++){
					var j=this.boxes[f];
					if(j.x<m.x+m.width&&m.x<j.x+j.width&&j.y<m.y+m.height&&m.y<j.y+j.height){
						break
					}
				}
				if(f==this.boxes.length){
					return k
				}
			}
			i++
		}
		return null
	};
	this.getPosition=function(e,f,d){
		var g=e;
		switch(f){
			case"n":
				g.y-=d;
				break;
			case"s":
				g.y+=d;
				break;
			case"e":
				g.x+=d;
				break;
			case"w":
				g.x-=d;
				break;
			case"ne":
				g.y-=d;
				g.x+=d;
				break;
			case"se":
				g.y+=d;
				g.x+=d;
				break;
			case"nw":
				g.y-=d;
				g.x-=d;
				break;
			case"sw":
				g.y+=d;
				g.x-=d;
				break
		}
		return g
	};
	this.extendBounds=function(e,d){
		e.minx=Math.min(d.x,e.minx);
		e.miny=Math.min(d.y,e.miny);
		e.maxx=Math.max(d.x+d.width,e.maxx);
		e.maxy=Math.max(d.y+d.height,e.maxy)
	};
	this.drawText=function(h,g,d,f,e){
		canvasport.drawText(e,h,d.x,d.y,f,g,this.stroke)
	};
	this.getOpacityvalue=function(e,d){
		if(this.shaded==false){
			return this.opacityvalue
		}
		else{
			return e/d*0.6+0.3
		}
	}
};

metaaps.nebulos.prototype={
	setSymbols:function(a){this.symbols=a},
	changeMostCommonWords:function(a){this.commonwords=a},
	setMinWordSize:function(a){this.minWordSize=a},
	restart:function(a){this.restarthandler=a},
	setFontFamily:function(a){this.fontfamily=a},
	draw:function(v,e){
		this.textlist=v;
		this.boxes=[];
		this.running=true;
		this.restarthandler=null;
		var d=this.canvas;
		var q=canvasport.getDrawing(d);
		q.clearRect(0,0,d.width,d.height);
		q.fillStyle="rgba(255, 255, 255, 1)";
		q.fillRect(0,0,d.width,d.height);
		var r={x:d.width/2,y:d.height/2};
		var g={minx:r.x,miny:r.y,maxx:r.x,maxy:r.y};
		function o(C,A){
			var w={x:(g.maxx+g.minx)/2,y:(g.maxy+g.miny)/2};
			var y={x:w.x-A.width/2,y:(a?w.y+A.height/2:w.y-A.height/2)};
			var z=g.maxx-g.minx;
			var i=g.maxy-g.miny;
			var C="";
			if(w.y>r.y){
				C+="n"
			}
			else{
				C+="s"
			}
			if(w.x>r.x){
				C+="w"
			}
			else{
				C+="e"
			}
			var B=(Math.random())*z/3;
			var x=(Math.random())*i/3;
			switch(C){
				case"ne":
					return{x:y.x+B,y:y.y-x};
					break;
				case"nw":
					return{x:y.x-B,y:y.y-x};
					break;
				case"se":
					return{x:y.x+B,y:y.y+x};
					break;
				case"sw":
					return{x:y.x-B,y:y.y+x};
					break
			}
		return null
		}
		var k=this.directions;
		var s=this;
		var a=0;
		this.textlistcount=0;
		q.textBaseline="top";
		q.strokeStyle=this.strokestyle;
		q.textAlign="left";
		var l={area:0};
		var n=10;
		var m=this.textlist;
		for(var t=0;t<m.length;t++){
			var u=m[t];
			var c=u.weight*n;
			q.font=c+"px "+s.fontfamily;
			var j=s.measureText(u.text,c,a,q);
			l.area+=j.width*j.height
		}
		var p=Math.sqrt((d.width*d.height)/l.area*s.screenportion)*n;
		var f=p*m[0].weight;
		var b="Could not place: ";
		function h(){
			var C=m[s.textlistcount++];
			var x=C.weight;
			var F=Math.floor(x*p);
			q.font=F+"px "+s.fontfamily;
			q.textBaseline="top";
			var A=s.getOpacityvalue(F,f);
			q.fillStyle="rgba("+s.fillstyle.red+", "+s.fillstyle.green+", "+s.fillstyle.blue+", "+A+")";
			q.strokeStyle=s.strokestyle;
			q.textAlign="left";
			var E=C.text;
			a=(Math.random()<0.5);
			var y=s.measureText(E,F,a,q);
			try{
				for(var i=0;i<4;i++,a=!a,y=s.measureText(E,F,a,q)){
					var B=Math.floor(Math.random()*4);
					var D=k[B];
					var w=s.findPosition(o(D,y),y,a,B,q);
					if(w!=null){
						s.drawText(E,q.font,w,a,q);
						s.boxes.push({x:w.x,y:(a?w.y-y.height:w.y),width:y.width,height:y.height,position:w,text:E,vertical:a,font:q.font,fillstyle:q.fillstyle,fontSize:F});
						break
					}
				}
				if(i==4){
					b+=" "+E
				}
				s.extendBounds(g,{x:w.x,y:(a?w.y-y.height:w.y),width:y.width,height:y.height})
			}
			catch(z){}
			if(s.restarthandler!=null){
				setTimeout(function(){s.restarthandler()},500);
				s.running=false;
				return
			}
			if(s.textlistcount<m.length){
				setTimeout(h,1)
			}
			else{
				s.running=false
			}
		}
		setTimeout(h,1)
	},
	redraw:function(){
		var c=this.canvas;
		var b=this;
		var a=canvasport.getDrawing(c);	
		a.clearRect(0,0,c.width,c.height);
		a.textBaseline="top";
		a.strokeStyle=b.strokestyle;
		a.textAlign="left";
		var g=b.boxes[0].fontSize;
		for(var d=0;d<b.boxes.length;d++){
			var f=b.boxes[d];
			var e=b.getOpacityvalue(f.fontSize,g);
			a.fillStyle="rgba("+b.fillstyle.red+", "+b.fillstyle.green+", "+b.fillstyle.blue+", "+e+")";
			b.drawText(f.text,f.font,f.position,f.vertical,a)
		}
	}
};

var canvasport={
	createCanvas:function(b,e,a,d){
		var c=document.createElement("canvas");
//		var c=b;
		b.appendChild(c);
		c.setAttribute('width',e);  
		c.setAttribute('height',a);  
//		c.style.margin="0px";
//		c.style.padding="0px";
		if(window.G_vmlCanvasManager){
			window.G_vmlCanvasManager.initElement(c)
		}
		return c
	},
	getDrawing:function(a){
		return a.getContext("2d")
	},
	_fillText:function(b,d,a,e,c){
		if(b.fillText){
			b.font=c;
			b.fillText(d,a,e)
		}
		else{
			if(b.mozDrawText){
				b.save();
				b.mozTextStyle=c;
				b.translate(a,e);
				b.mozDrawText(d);
				b.restore()
			}
		}
	},
	_strokeText:function(b,d,a,e,c){
		if(b.strokeText){
			b.font=c;
			b.strokeText(d,a,e)
		}
		else{
			if(b.mozDrawText){
				b.save();
				b.mozTextStyle=c;
				b.translate(a,e);
				b.mozDrawText(d);
				b.restore()
			}
		}
	},
	drawText:function(b,f,a,g,d,c,e){
		if(d){
			b.save();
			b.translate(a,g);
			b.rotate(270*Math.PI/180);
			this._fillText(b,f,0,0,c);
			if(e){
				this._strokeText(b,f,0,0,c)
			}
			b.restore()
		}
		else{
			this._fillText(b,f,a,g,c);
			if(e){
				this._strokeText(b,f,a,g,c)
			}
		}
	},
	measureText:function(a,b){
		return(a.measureText?a.measureText(b).width:(a.mozMeasureText?a.mozMeasureText(b):100))
	},
	drawImage:function(m,f,b,a,d,k,h,g,c,l){
		try{
			var i=f[0];
			m.drawImage(i,b,a,d,k,h,g,c,l)
		}
		catch(j){
			alert("Problem with canvas "+j.message)
		}
	},
	drawImageslice:function(a,d,g){
		try{
			var c=d;
			var b=g;
			if(this.spriteimage!=null){
				a.drawImage(this.spriteimage,c.x,0,c.w,c.h,b.x-Math.floor(c.w/2),b.y-Math.floor(c.h/2),c.w,c.h)
			}
		}
		catch(f){
			llh.error("Problem with canvas "+f.message)
		}
	},
	roundedRect:function(k,h,g,a,j,f,m,c,e,l){
		var b=7;
		var d=(j-b)/2;
		function i(n){
			return(c?n+h:a+h-n)
		}
		k.beginPath();
		k.moveTo(i(0),g+e);
		k.lineTo(i(0),g+d-b/2);
		k.quadraticCurveTo(i(-h),g+d-b/2,f.x,f.y);
		k.quadraticCurveTo(i(-h),g+d+b/2,i(0),g+d+b/2);
		k.lineTo(i(0),g+j-e);
		k.quadraticCurveTo(i(0),g+j,i(e),g+j);
		k.lineTo(i(a-e),g+j);
		k.quadraticCurveTo(i(a),g+j,i(a),g+j-e);
		k.lineTo(i(a),g+e);
		k.quadraticCurveTo(i(a),g,i(a-e),g);
		k.lineTo(i(e),g);
		k.quadraticCurveTo(i(0),g,i(0),g+e);
		k.closePath();
		k.strokeStyle=(l&&l.color?l.color:"#723F3F");
		k.fillStyle=(l&&l.bkcolor?l.bkcolor:"rgba(255, 255, 255, 1.0)");
		k.fill();
		k.stroke()
	},
	customiseBubble:function(c,d,b,f,e){
		var a=d.position();
		a.top+=parseInt(d.css("padding-top").replace("px",""));
		a.left+=parseInt(d.css("padding-left").replace("px",""));
		var h=5;
		c.clearRect(0,0,c.canvas.width,c.canvas.height);
		var g={x:(f?0:c.canvas.width),y:(b?0:c.canvas.height)};
		this.roundedRect(c,a.left-h,a.top-h,d.width()+2*h,d.height()+2*h,g,b,f,15,e)
	},
	hitTest:function(j,k,h,b,m,a){
		var g=j.canvas.width;
		var f=j.canvas.height;
		if(a){
			if((k<0)||(h<0)||(k+b>g)||(h+m>f)){
				return true
			}
		}
		var l=j.getImageData(k,h,b,m);
		var d=l.data;
		for(var e=0,c=d.length;e<c;e+=4){
			if(d[e]!=255){
				return true
			}
		}
		return false}};

