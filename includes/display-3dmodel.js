import * as THREE from '../includes/three.js/three.module.js';  // three.jsのモジュールをインポート
import { STLLoader } from '../includes/three.js/STLLoader.js';  // STLLoaderモジュールをインポート
import { OrbitControls } from '../includes/three.js/OrbitControls.js';  // OrbitControlsモジュールをインポート


// 主要な色の名前を引数とし、その色のコード(16進数)を返す関数
function name2colorValue(color) {
    let color_code = 0x00ffff; // 初期値として水色のコードを指定

    if (color === "red") {
        color_code = 0xff0000; // 赤色のコードを指定
    } else if (color === "green") {
        color_code = 0x00ff00; // 緑色のコードを指定
    } else if (color === "blue") {
        color_code = 0x0000ff; // 青色のコードを指定
    } else if (color === "white") {
        color_code = 0xf8f8f8; // 白色のコードを指定
    } else if (color === "gray" ||color === "grey") {
        color_code = 0x808080; // 灰色のコードを指定
    } else if (color === "black") {
        color_code = 0x000000; // 黒色のコードを指定
    } else if (color === "pink") {
        color_code = 0xffc0cb; // ピンクのコードを指定
    } else if (color === "orange") {
        color_code = 0xf5871f; // オレンジのコードを指定
    } else if (color === "yellow") {
        color_code = 0xffff00; // 黄色のコードを指定
    }
    
    return color_code;
}


// 表示する形状ファイルのクラス
class CubicModel {
    // 初期化(レンダラー、シーン、カメラを取得)
    constructor(file_path, element_id, camera_position, color, distance_limit) {
        // near_limit: この距離より手前のオブジェクトは描画されない [3D空間の長さ単位]
        // far_limit:  この距離より奥のオブジェクトは描画されない [3D空間の長さ単位]
        
        const [object_color, background_color] = color;
        const [near_limit, far_limit] = distance_limit;
        
        const container = document.getElementById(element_id); // 表示先のdiv要素の設定
        
        // カメラ
        const fov = 5; // 視野角（垂直方向）[deg] 
        const aspect = container.clientWidth / container.clientHeight; // カメラのアスペクト比 (横/縦) [-]
        this.camera = new THREE.PerspectiveCamera(fov, aspect, near_limit, far_limit); // カメラを作成
        this.camera.position.set(camera_position[0], camera_position[1], camera_position[2]);  // カメラの位置を設定
        
        // シーン
        this.scene = new THREE.Scene();  // シーンを作成
        this.scene.background = new THREE.Color( name2colorValue(background_color) ); // シーンの背景色を設定
        let ambientLight = new THREE.AmbientLight(name2colorValue('white'), 0.1);  // 環境光を作成（色、強度を指定）
        this.scene.add(ambientLight);  // シーンに環境光を追加
        
        const directionalLight = new THREE.DirectionalLight(name2colorValue('white'), 1.2); // 強い平行光（白色）
        directionalLight.position.set(1, 1, 1); // 光の方向を設定
        this.scene.add(directionalLight);
        
        
        // STLファイルの読み込み
        const self = this; // thisの参照を保持
        new STLLoader().load(file_path, function (geometry) {
            // STLファイルが読み込まれた後に実行されるコールバック関数
            
            // 3Dオブジェクトのマテリアルを設定
            if (object_color === "rainbow") {
                var material = new THREE.MeshNormalMaterial(); 
            } else {
                var material = new THREE.MeshPhongMaterial({ color: name2colorValue(object_color) });
            };
            var object = new THREE.Mesh(geometry, material); // 3Dオブジェクトを作成
            object.position.set(0, 0, 0); // 3Dオブジェクトの位置を設定
            self.scene.add(object); // シーンに3Dオブジェクトを追加
        });
        
        // レンダラー
        this.renderer = new THREE.WebGLRenderer({ antialias: true });  // WebGLRendererを作成（アンチエイリアスを有効にする）
        this.renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(this.renderer.domElement);  // レンダラーのDOM要素を追加
        
        let controls = new OrbitControls(this.camera, this.renderer.domElement);  // カメラコントロールを作成（カメラ、コントロール対象の要素を指定）
    };
    
    animate() {
        const self = this; // thisの参照を保持
        requestAnimationFrame(function() {
            self.animate(); // アニメーションフレームの更新をリクエスト
        });
        this.renderer.render(this.scene, this.camera); // シーンをレンダリング
    };
}


// メイン処理
// OBJ_INFO(形状ファイルの表示設定)はhtmlコード内で定義
let cm=[];

for (let i = 0; i < OBJ_INFO.length; i++) {
    const [file_path, element_id_arr, camera_position_arr, color_arr, distance_limit] = OBJ_INFO[i];
    
    for (let j = 0; j < element_id_arr.length; j++) {
        cm[i] = new CubicModel(file_path, element_id_arr[j], camera_position_arr[j], color_arr[j], distance_limit);
        cm[i].animate();
    }
}
