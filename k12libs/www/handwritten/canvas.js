const clearBtnDOM = document.getElementById('clearButton');
const saveNumberBtnDOM = document.getElementById('saveNumberButton');
const resultDOM = document.getElementsByClassName("content-result")[0];
const newPDOM = document.createElement("p");
const pDOM = document.getElementsByClassName("content-result-text")[0];
const loadingDOM = document.getElementsByClassName("loading")[0];

const canvasDOM = document.getElementById('the_stage');
const ctx = canvasDOM.getContext('2d');
const urlParams = new URLSearchParams(window.location.search);

const mnistPad = new SignaturePad(canvasDOM, {
	backgroundColor: 'black',
	minWidth: 8,
	maxWidth: 9,
	penColor: 'white',
	length:50
});

clearBtnDOM.addEventListener('click', function(event) {
	pDOM.style.lineHeight = '1.08rem';
	resultDOM.removeChild(newPDOM);
	mnistPad.clear();
});

saveNumberBtnDOM.addEventListener('click', function(event) {
	if (mnistPad.isEmpty()) {
		alert('请先写入');
	} else {
		loadingDOM.style.display = "block";
		img2text();
	}
});

function img2text() {
	const dataTemp = mnistPad.toDataURL('image/png');

    let host = "116.85.5.40";
    let port = "9119";
    let num_classes = 10;
    let label_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    let ckpt_path = "/raceai/data/ckpts/rmnist/pl_resnet18_rotation.pth";
    if (urlParams.has("host")) {
        host = urlParams.get("host");
    }
    if (urlParams.has("port")) {
        port = urlParams.get("host");
    }
    if (urlParams.has("num_classes")) {
        num_classes = parseInt(urlParams.get("num_classes"));
    }
    if (urlParams.has("ckpt_path")) {
        ckpt_path = urlParams.get("ckpt_path");
        if (ckpt_path.indexOf('letters')) {
            label_names = ['a/A', 'b/B', 'c/C', 'd/D', 'e/E', 'f/F', 'g/G',
                'h/H', 'i/I', 'j/J', 'k/K', 'l/L', 'm/M', 'n/N',
                'o/O', 'p/P', 'q/Q', 'r/R', 's/S', 't/T',
                'u/U', 'v/V', 'w/W',
                'x/X', 'y/Y', 'z/Z']
        }
    }

    console.log(ckpt_path)

	const request = new XMLHttpRequest();
	request.onreadystatechange = function() {
		if (request.readyState === 4) {
			if ((request.status >= 200 && request.status < 300) || request.status === 304) {
				let ret = JSON.parse(request.response);
                console.log(ret)
				if(ret.errno === 0){
					pDOM.style.lineHeight = '0.5rem';
					newPDOM.innerText = label_names[ret.result[0].probs_sorted.indices[0]];
					newPDOM.style.fontSize = "0.25rem";
					newPDOM.style.lineHeight = "0.3rem";
					loadingDOM.style.display = "none";
					resultDOM.appendChild(newPDOM);
				} else {
					loadingDOM.style.display = "none";
					newPDOM.innerText = "Error";
                }
			};
		}
	};

    var reqdata = {
        "task": "cls.inference.pl",
        "cfg": {
            "data": {
                "class_name": "raceai.data.process.Base64DataLoader",
                "params": {
                    "data_source": dataTemp,
                    "dataset": {
                        "class_name": "raceai.data.PredictListImageDataset",
                        "params": {
                            "input_size": 28,
                            "mean": [0.1362, 0.1362, 0.1362],
                            "std": [0.2893, 0.2893, 0.2893]
                        }
                    },
                    "sample": {
                        "batch_size": 32,
                        "num_workers": 4,
                    }
                }
            },
            "model": {
                "class_name": "raceai.models.backbone.Resnet18",
                "params": {
                    "device": 'gpu',
                    "num_classes": num_classes,
                    "weights": false
                }
            },
            "trainer": {
                "default_root_dir": "/raceai/data/tmp/resnet18",
                "gpus": 1,
                "resume_from_checkpoint": ckpt_path
            }
        }
    };
    restapi = "http://" + host + ":" + port + "/raceai/framework/inference"
	request.open("POST", restapi);
	request.send(JSON.stringify(reqdata));
}
function resizeCanvas() {
	// const ratio = Math.max(window.devicePixelRatio || 1, 1);
	setTimeout(() => {
		canvasDOM.width = canvasDOM.offsetWidth;
		canvasDOM.height = canvasDOM.offsetHeight;
		mnistPad.clear();
	}, 1000);
//  canvas.getContext("2d").scale(ratio, ratio);
};

window.onresize = resizeCanvas;
resizeCanvas();
