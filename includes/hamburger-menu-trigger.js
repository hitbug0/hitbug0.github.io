$(".hm-trigger").click(function () {//ボタンがクリックされたら
	$(this).toggleClass('active');//ボタン自身に activeクラスを付与し
    $("#hm-nav").toggleClass('panelactive');//ナビゲーションにpanelactiveクラスを付与
});

$("#hm-nav a").click(function () {//ナビゲーションのリンクがクリックされたら
    $(".hm-trigger").removeClass('active');//ボタンの activeクラスを除去し
    $("#hm-nav").removeClass('panelactive');//ナビゲーションのpanelactiveクラスも除去
});