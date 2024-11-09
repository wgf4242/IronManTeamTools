import sjcl from './sjcl.js';
var maxMessageSize = 1000;

var importImage = function(e) {
    var reader = new FileReader();

    reader.onload = function(event) {
        var img = new Image();
        img.onload = function() {
            var ctx = document.getElementById('canvas').getContext('2d');
            ctx.canvas.width = img.width;
            ctx.canvas.height = img.height;
            ctx.drawImage(img, 0, 0);

        };
        img.src = event.target.result;
    };

    reader.readAsDataURL(e);
};

var decode = function(password) {
    var passwordFail = 'Password is incorrect or there is nothing here.';
    var ctx = document.getElementById('canvas').getContext('2d');
    var imgData = ctx.getImageData(0, 0, ctx.canvas.width, ctx.canvas.height);
    var message = decodeMessage(imgData.data, sjcl.hash.sha256.hash(password));

    var obj = null;
    try {
        obj = JSON.parse(message);
    } catch (e) {

        if (password.length > 0) {
            alert(passwordFail);
        }
    }

    if (obj) {
        if (obj.ct) {
            try {
                obj.text = sjcl.decrypt(password, message);
            } catch (e) {
                alert(passwordFail);
            }
        }

        var escChars = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            '\'': '&#39;',
            '/': '&#x2F;',
            '\n': '<br/>'
        };
        var escHtml = function(string) {
            return String(string).replace(/[&<>"'\/\n]/g, function (c) {
                return escChars[c];
            });
        };
        return obj.text;
        // document.getElementById('messageDecoded').innerHTML = escHtml(obj.text);
    }
};

var getBit = function(number, location) {
    return ((number >> location) & 1);
};

var setBit = function(number, location, bit) {
    return (number & ~(1 << location)) | (bit << location);
};


var getNumberFromBits = function(bytes, history, hash) {
    var number = 0, pos = 0;
    while (pos < 16) {
        var loc = getNextLocation(history, hash, bytes.length);
        var bit = getBit(bytes[loc], 0);
        number = setBit(number, pos, bit);
        pos++;
    }
    return number;
};


var getNextLocation = function(history, hash, total) {
    var pos = history.length;
    var loc = Math.abs(hash[pos % hash.length] * (pos + 1)) % total;
    // eslint-disable-next-line no-constant-condition
    while (true) {
        if (loc >= total) {
            loc = 0;
        } else if (history.indexOf(loc) >= 0) {
            loc++;
        } else if ((loc + 1) % 4 === 0) {
            loc++;
        } else {
            history.push(loc);
            return loc;
        }
    }
};

var decodeMessage = function(colors, hash) {
    var history = [];

    var messageSize = getNumberFromBits(colors, history, hash);

    if ((messageSize + 1) * 16 > colors.length * 0.75) {
        return '';
    }

    if (messageSize === 0 || messageSize > maxMessageSize) {
        return '';
    }

    var message = [];
    for (var i = 0; i < messageSize; i++) {
        var code = getNumberFromBits(colors, history, hash);
        message.push(String.fromCharCode(code));
    }

    return message.join('');
};

export {importImage, decode}
