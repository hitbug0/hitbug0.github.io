// 各ボタンに対してClipboardJSを初期化する
var buttons = document.querySelectorAll('.copy-button');
buttons.forEach(function(button) {
    var clipboard = new ClipboardJS(button, {
        text: function(trigger) {
            var targetSelector = trigger.getAttribute('data-clipboard-target');
            var textToCopy = document.querySelector(targetSelector).innerText.trim();
            var lines = textToCopy.split('\n').slice(1);
            var modifiedText = lines.join('\n');
            return modifiedText;
        }
    });
    
    clipboard.on('success', function(e) {
        console.log('Text copied to clipboard:', e.text);
        e.clearSelection();

        // コピーが成功したら2秒間だけボタンのテキストを変更する
        button.textContent = 'Copied!';
        setTimeout(function() {
            button.textContent = 'Copy';
        }, 2000);
    });

    clipboard.on('error', function(e) {
        console.error('Failed to copy text to clipboard:', e.action);
    });
});