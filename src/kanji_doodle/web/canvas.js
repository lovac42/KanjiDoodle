// Copyright (C) 2019 Lovac42
// Copyright (C) 2018-2019 Michal Krassowski <krassowski.michal@gmail.com>
// Support: https://github.com/lovac42/KanjiDoodle
// License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


// console.log("device="+DEVICE);

var visible = false;
var saveMode = false;
var isMouseDown = false;
var pos = {x:0, y:0};
var lst_pos = {x:0, y:0};
var op_stack = [];

var canvas_wrapper = document.getElementById('canvas_wrapper');
var ts_crop_field = document.getElementById('ts_crop_field');
var ts_toggle_button = document.getElementById('ts_toggle_button');
var ts_save_button = document.getElementById('ts_save_button');
var ts_undo_button = document.getElementById('ts_undo_button');
var canvas = document.getElementById('ts_canvas');
var ctx = canvas.getContext('2d');


canvas.onselectstart = function() {
    return false;
};

function init(){
    var w=window.innerWidth/4;
    var h=window.innerHeight/4;
    ts_crop_field.style.left=w+'px';
    ts_crop_field.style.top=h+'px';
    ts_crop_field.style.width=w*2+'px';
    ts_crop_field.style.height=h*2+'px';
    resize();
}

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
    if($(ts_save_button).hasClass("active")) {
        if(saveMode){
            sx=parseInt(ts_crop_field.style.left);
            sy=parseInt(ts_crop_field.style.top);
            sw=parseInt(ts_crop_field.style.width);
            sh=parseInt(ts_crop_field.style.height);
            tmpImg=ctx.getImageData(sx,sy,sw,sh);

            ctx.canvas.width=sw;
            ctx.canvas.height=sh;
            ctx.putImageData(tmpImg,0,0);
            data=canvas.toDataURL('image/png',1);
            resize();
            tsCallback.saveCanvas(data);
            toggleSaveMode(true);
        }else{
            tsCallback.tooltip("Select save area");
            toggleSaveMode();
        }
    }
}

function toggleSaveMode(reset){
    if(saveMode || reset){
        saveMode=false;
        ts_crop_field.hidden=1;
        $(ts_save_button).removeClass('save');
    }else{
        saveMode=true;
        ts_crop_field.hidden=0;
        $(ts_save_button).addClass('save');
    }
}

function switch_off_buttons(turn_off) {
    if(turn_off){
        canvas_wrapper.style.display = 'none';
        toggleSaveMode(true);
    } else {
        canvas_wrapper.style.display = 'block';
        tsCallback.signal(visible);
    }
    tsCallback.signal(false);
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
        toggleSaveMode(true);
}

function resize() {
    // var card = document.getElementsByClassName('card')[0]
    // ctx.canvas.width = document.documentElement.scrollWidth - 1;
    ctx.canvas.height = Math.max(
        document.body.clientHeight,
        window.innerHeight
        // document.documentElement ? document.documentElement.scrollHeight : 0,
        // card ? card.scrollHeight : 0
    // ) - 1;
    );
    canvas.width = window.innerWidth;
    // canvas.height = window.innerHeight;
    ts_redraw();
}

function clear_canvas(reset) {
    if(visible || reset){
        if(op_stack.length){
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            op_stack = [];
            ts_undo_button.className = "";
            ts_save_button.className = "";
            canvas.style.display = 'block';
            toggleSaveMode(true);
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
    update_pen_settings();
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
    return {x:e.pageX, y:e.pageY};
}

function calCropField(x,y) {
    var sx = Math.min(ts_crop_field.x,x);
    var sw = Math.max(ts_crop_field.x,x);
    var sy = Math.min(ts_crop_field.y,y);
    var sh = Math.max(ts_crop_field.y,y);
    ts_crop_field.style.left = sx + 'px';
    ts_crop_field.style.top = sy + 'px';
    ts_crop_field.style.width = sw - sx + 'px';
    ts_crop_field.style.height = sh - sy + 'px';
}



$('input').on(DEVICE+'down', function(e) {
    e.preventDefault(); //prevent focus on btn clicks
});

window.addEventListener(DEVICE+"up", function (e) {
    isMouseDown=false;
    if(live_update)
        ts_redraw();
});

window.addEventListener(DEVICE+"out", function (e) {
    isMouseDown=false;
    if(live_update)
        ts_redraw();
});

canvas.addEventListener(DEVICE+"down", function (e) {
    if(!visible || e.which!==1) return;
    e.preventDefault();
    isMouseDown=true;
    pos=lst_pos=getMousePos(e);
    if(saveMode){
        ts_crop_field.x=pos.x;
        ts_crop_field.y=pos.y;
    }else{
        update_pen_settings();
        var dot={x:pos.x,y:pos.y-1};
        op_stack.push(new Array());
        lst=op_stack.length-1 //dynamic
        op_stack[lst].push([ts_color,ts_width]);
        op_stack[lst].push(dot);
        op_stack[lst].push(pos);
        ts_draw(dot.x,dot.y,pos.x,pos.y);
        ts_undo_button.className = "active";
        ts_save_button.className = "active";
    }
});

canvas.addEventListener(DEVICE+"move", function (e) {
    pos=getMousePos(e);
    if(saveMode && isMouseDown && visible) {
        calCropField(pos.x,pos.y);
    }
});



setTimeout(init,0); //sets init card in reviewer
window.addEventListener('resize', resize);
document.body.addEventListener('load', init);


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
    if(!saveMode && isMouseDown && visible) {
        lst=op_stack.length-1 //dynamic
        op_stack[lst].push(pos);

        ts_draw(lst_pos.x,lst_pos.y,pos.x,pos.y);
        lst_pos=pos;
    }
};

(function start() {
    updateCanvas();
    requestAnimationFrameWrapper(start);
})();
