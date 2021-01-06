(function () {
	const contentUploadDOM = document.getElementsByClassName("content-upload")[0];
	const uploadImageInputDOM = document.getElementById("uploadImage");
	const uploadImageDOM = document.getElementsByClassName("content-upload-image")[0];
	const uploadTextDOM = document.getElementsByClassName("content-upload-text")[0];
	const resultDOM = document.getElementsByClassName("content-result")[0];
	const resultTextDOM = document.getElementsByClassName("content-result-text")[0];
	const loadingDOM = document.getElementsByClassName("loading")[0];
    // const resultTextDisplayDOM = document.getElementsByClassName("content-result-display")[0];

	contentUploadDOM.onclick = (e) => {
		uploadImageInputDOM.click();
	}

	if (uploadImageInputDOM) {
		uploadImageInputDOM.onchange = (e) => {
			const file = uploadImageInputDOM.files[0];
			const reader = new FileReader();
			reader.readAsDataURL(file);
			reader.onload = function () {
				deleteResult();
				uploadTextDOM.style.display = "none";
				uploadImageDOM.style.display = "block";
				uploadImageDOM.src = this.result;
				uploadImageDOM.onload = function () {
					const canvas = document.createElement("canvas");
					const context = canvas.getContext('2d');
					canvas.width = 224;
					canvas.height = 224;
					context.drawImage(uploadImageDOM, 0, 0, 224, 224);
					window.fileBase64 = canvas.toDataURL();
				}
			}
		}
	}

	function deleteResult() {
		uploadTextDOM.style.display = "block";
		uploadImageDOM.style.display = "none";
		uploadImageDOM.src = '';
		uploadImageInputDOM.value = '';
		window.fileBase64 = null;
		resultTextDOM.style.lineHeight = '1.08rem';
		loadingDOM.style.display = "none";
		// resultTextDisplayDOM.style.display = "none";
		if (resultDOM.children.length > 1) {
			resultDOM.removeChild(resultDOM.children[resultDOM.children.length - 1])
		}
	}

	const deleteButtonDOM = document.getElementById("deleteButton");
	if (deleteButtonDOM) {
		deleteButtonDOM.onclick = function () {
			deleteResult();
		}
	}

})(window)
