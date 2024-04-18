const fileInput = document.querySelector(".file-input");
filterOptions = document.querySelectorAll(".filter button");
filterName = document.querySelector(".filter-info .name");
previewImg = document.querySelector(".preview-img img");
saveImgBtn = document.querySelector(".save-img");
chooseImgBtn = document.querySelector(".choose-img");
let rotate = 0, flipHorizontal = 1, flipVertical = 1;
rotateOptions = document.querySelectorAll(".options button");
const file2 = document.querySelector(".bgraund");
choseBG = document.querySelector(".upload");

const applyFilter = () => {
    previewImg.style.transform = `rotate(${rotate}deg) scale(${flipHorizontal}, ${flipVertical})`;
}

const loadImage = () => {
    let file = fileInput.files[0];
    if(!file) return;
    previewImg.src = URL.createObjectURL(file);
    previewImg.addEventListener("load", () => {
        resetFilterBtn.click();
        document.querySelector(".container").classList.remove("disable");
    });
}

rotateOptions.forEach(option => {
    option.addEventListener("click", () => {
        if(option.id === "left") {
            rotate -= 45;
        } else if(option.id === "right") {
            rotate += 45;
        } else if(option.id === "horizontal") {
            flipHorizontal = flipHorizontal === 1 ? -1 : 1;
        } else {
            flipVertical = flipVertical === 1 ? -1 : 1;
        }
        applyFilter();
    });
});

fileInput.addEventListener("change", loadImage);
chooseImgBtn.addEventListener("click", () => fileInput.click());
choseBG.addEventListener("click", () => file2.click());
// function applyBackground() {
//     var bgColor = document.getElementById('bg-color').value;
//     var bgImage = document.getElementById('bg-image').files[0];
//     var previewImg = document.querySelector('.preview-img');

//     // Apply background color
//     previewImg.style.backgroundColor = bgColor;

//     // Apply background image if selected
//     if (bgImage) {
//         var reader = new FileReader();
//         reader.onload = function (e) {
//             previewImg.style.backgroundImage = 'url(' + e.target.result + ')';
//         }
//         reader.readAsDataURL(bgImage);
//     }
// }
