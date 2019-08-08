// Copyright (C) 2019 Lovac42
// Copyright (C) 2018-2019 Michal Krassowski <krassowski.michal@gmail.com>
// Support: https://github.com/lovac42/TouchScreenEvo
// License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


// console.log("device="+DEVICE);

var visible = false;
var isMouseDown = false;
var pos = {x:0, y:0};
var lst_pos = {x:0, y:0};
var op_stack = [];

var canvas_wrapper = document.getElementById('canvas_wrapper');
var ts_toggle_button = document.getElementById('ts_toggle_button');
var ts_save_button = document.getElementById('ts_save_button');
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
    // ctx.fillStyle = ts_color;
}

function change_color(){
    if(visible){
        tsCallback.chooseColor();
    }
}

function change_stroke(){
    if(visible){
        tsCallback.chooseWidth();
    }
}

function save_canvas(){
    if(ts_save_button.className==="active"){
        data=canvas.toDataURL('image/png',1);
        tsCallback.saveCanvas(data);
    }
}

function switch_off_buttons(turn_off) {
    if(turn_off){
        canvas_wrapper.style.display = 'none';
        tsCallback.signal(false);
    } else {
        canvas_wrapper.style.display = 'block';
        tsCallback.signal(visible);
    }
}

function init_visibility(signal) {
    switch_visibility(signal);
}

function switch_visibility(signal) {
    visible = !visible;
    if(visible){
        canvas.style.display = 'block';
        $(ts_toggle_button).addClass('active').siblings().css({"display":"inherit"});
    }else{
        canvas.style.display = 'none';
        $(ts_toggle_button).removeClass('active').siblings().css({"display":"none"});
    }

    if(signal)
        tsCallback.signal(visible);
}

function resize() {
    var card = document.getElementsByClassName('card')[0]
    // ctx.canvas.width = document.documentElement.scrollWidth - 1;
    // ctx.canvas.height = Math.max(
        // document.body.clientHeight,
        // window.innerHeight,
        // document.documentElement ? document.documentElement.scrollHeight : 0,
        // card ? card.scrollHeight : 0
    // ) - 1;
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    ts_redraw()
}

function clear_canvas(reset) {
    if(visible || reset){
        if(op_stack.length){
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            op_stack = [];
            ts_undo_button.className = "";
            ts_save_button.className = "";
            canvas.style.display = 'block';
        }
    }
}

function ts_undo() {
    if(!visible) return;
    op_stack.pop()
    if(!op_stack.length) {
        ts_undo_button.className = "";
        ts_save_button.className = "";
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
    // update_pen_settings();
    for(var p=0; p<op_stack.length; p++) {
        ctx.strokeStyle = op_stack[p][0][0];
        ctx.lineWidth = op_stack[p][0][1];
        var p1 = op_stack[p][1];
        var p2 = op_stack[p][2];
        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        for(var i=2,L=op_stack[p].length; i<L; i++) {
            var mp = midPointBtw(p1, p2);
            ctx.quadraticCurveTo(p1.x, p1.y,mp.x,mp.y);
            p1 = op_stack[p][i];
            p2 = op_stack[p][i+1];
        }
        ctx.lineTo(p1.x, p1.y);
        ctx.stroke();
        // ctx.fill();
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

$('input').on(DEVICE+'down', function(e) {
    e.preventDefault(); //prevent focus on btn clicks
});

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
    update_pen_settings();
    lst_pos=pos=getMousePos(e);
    var dot={x:pos.x,y:pos.y-1};
    op_stack.push(new Array());
    lst=op_stack.length-1 //dynamic
    op_stack[lst].push([ts_color,ts_width]);
    op_stack[lst].push(dot);
    op_stack[lst].push(pos);
    ts_draw(dot.x,dot.y,pos.x,pos.y);
    ts_undo_button.className = "active";
    ts_save_button.className = "active";
});

canvas.addEventListener(DEVICE+"move", function (e) {
    if(isMouseDown && visible) {
        pos=getMousePos(e);
        lst=op_stack.length-1 //dynamic
        op_stack[lst].push(pos);
    }
});


setTimeout(resize,0); //sets init card in reviewer
window.addEventListener('resize', resize);
document.body.addEventListener('load', resize);


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
