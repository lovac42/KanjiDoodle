// Copyright (C) 2019 Lovac42
// Copyright (C) 2018-2019 Michal Krassowski <krassowski.michal@gmail.com>
// Support: https://github.com/lovac42/TouchScreenEvo
// License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


// console.log("device="+DEVICE);

var visible = false;
var isMouseDown = false;
var pos = {x:0, y:0};
var lst_pos = {x:0, y:0};
var arrays_of_points = [];

var ts_undo_button = document.getElementById('ts_undo_button');
var canvas = document.getElementById('ts_canvas');
var ctx = canvas.getContext('2d');


canvas.onselectstart = function () {
    return false;
};

function update_pen_settings() {
    ctx.lineJoin = ctx.lineCap = 'round';
    ctx.lineWidth = ts_width;
    ctx.strokeStyle = ts_color;
}

function switch_visibility() {
    if(visible) {
        canvas.style.display = 'none';
    } else {
        canvas.style.display = 'block';
    }
    visible = !visible;
}

function switch_off_buttons(turn_off) {
    var el=document.getElementById('canvas_wrapper');
    if(turn_off){
        el.style.display = 'none';
    } else {
        el.style.display = 'block';
    }
}

function switch_class(e, c) {
    var reg = new RegExp('(\\\s|^)' + c + '(\\s|$)');
    if(e.className.match(new RegExp('(\\s|^)' + c + '(\\s|$)'))) {
        e.className = e.className.replace(reg, '');
    } else {
        e.className += c;
    }
}

function resize() {
    var card = document.getElementsByClassName('card')[0]
    ctx.canvas.width = document.documentElement.scrollWidth - 1;
    ctx.canvas.height = Math.max(
        document.body.clientHeight,
        window.innerHeight,
        document.documentElement ? document.documentElement.scrollHeight :
        0,
        card ? card.scrollHeight : 0
    ) - 1;
    ts_redraw()
}

function clear_canvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    arrays_of_points = [];
    ts_undo_button.className = "";
    canvas.style.display = 'block';
}

function ts_undo() {
    arrays_of_points.pop()
    if(!arrays_of_points.length) {
        ts_undo_button.className = "";
    }
    canvas.style.display = 'block';
    ts_redraw()
}

function midPointBtw(p1, p2) {
    return {
        x: p1.x + (p2.x - p1.x) / 2,
        y: p1.y + (p2.y - p1.y) / 2
    };
}

function ts_redraw() {
    ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);
    update_pen_settings();
    for(var p=0; p<arrays_of_points.length; p++) {
        var p1 = arrays_of_points[p][0];
        var p2 = arrays_of_points[p][1];
        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        for(var i=1,L=arrays_of_points[p].length; i<L; i++) {
            var mp = midPointBtw(p1, p2);
            ctx.quadraticCurveTo(p1.x, p1.y,mp.x,mp.y);
            p1 = arrays_of_points[p][i];
            p2 = arrays_of_points[p][i+1];
        }
        ctx.lineTo(p1.x, p1.y);
        ctx.stroke();
    }
}

function ts_draw(fromX,fromY,toX,toY) {
    ctx.beginPath();
    ctx.moveTo(fromX,fromY);
    ctx.lineTo(toX,toY);
    ctx.stroke();
}

function getMousePos(e) {
    return {x:e.offsetX, y:e.offsetY};
}


window.addEventListener(DEVICE+"up", function (e) {
    isMouseDown = false;
    ts_redraw();
});

window.addEventListener(DEVICE+"out", function (e) {
    isMouseDown = false;
    ts_redraw();
});

canvas.addEventListener(DEVICE+"down", function (e) {
    if(!visible || e.which!==1) return;
    e.preventDefault();
    isMouseDown = true;
    lst_pos=pos=getMousePos(e);
    var dot={x:pos.x-1,y:pos.y-1};
    arrays_of_points.push(new Array());
    arrays_of_points[arrays_of_points.length-1].push(dot);
    arrays_of_points[arrays_of_points.length-1].push(pos);
    ts_draw(dot.x,dot.y,pos.x,pos.y);
    ts_undo_button.className = "active";
    update_pen_settings();
});

canvas.addEventListener(DEVICE+"move", function (e) {
    if(isMouseDown && visible) {
        pos=getMousePos(e);
        arrays_of_points[arrays_of_points.length-1].push(pos);
    }
});


window.addEventListener('resize', resize);
document.body.addEventListener('load',function(){
    setTimeout(resize,10);
},false);



// Uses requestAnimationFrame to animate
window.requestAnimationFrameWrapper = (function (callback) {
    return window.requestAnimationFrame || 
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame ||
        window.oRequestAnimationFrame ||
        window.msRequestAnimaitonFrame ||
        function (callback) {
            window.setTimeout(callback, 1000/60);
        };
})();

function updateCanvas() {
    if(isMouseDown && visible) {
        ts_draw(lst_pos.x,lst_pos.y,pos.x,pos.y);
        lst_pos=pos;
    }
};

(function start() {
    updateCanvas();
    requestAnimationFrameWrapper(start);
})();
