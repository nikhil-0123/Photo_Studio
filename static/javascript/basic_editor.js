const fileInput = document.querySelector(".file-input");
filterOptions = document.querySelectorAll(".filter button");
filterName = document.querySelector(".filter-info .name");
previewImg = document.querySelector(".preview-img img");
saveImgBtn = document.querySelector(".save-img");
chooseImgBtn = document.querySelector(".choose-img");
let rotate = 0, flipHorizontal = 1, flipVertical = 1;
rotateOptions = document.querySelectorAll(".options button");

const applyFilter = () => {
    previewImg.style.transform = `rotate(${rotate}deg) scale(${flipHorizontal}, ${flipVertical})`;
    previewImg.style.filter = filterStyles.trim();

}

const loadImage = () => {
    let file = fileInput.files[0];
    if(!file) return;
    previewImg.src = URL.createObjectURL(file);
    previewImg.addEventListener("load", () => {
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



function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $("#img").attr("src", e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function pcnt(x, name) {
    $(name).html(Math.round(x * 100) + "%");
}
function blr(x) {
    $("#blr").html(x + "px");
}
function hr(x) {
    $("#hr").html(x + "deg");
}
$(document).change(function (e) {
    let brt = $(".brt").val();
    let cnt = $(".cnt").val();
    let gs = $(".gs").val();
    let inv = $(".inv").val();
    let opa = $(".opa").val();
    let sat = $(".sat").val();
    let sep = $(".sep").val();
    let blr = $(".blr").val();
    let hr = $(".hr").val();

     brt1 = brt
     cnt2 = cnt
     gs3 = gs
     inv4 = inv
     opa5 = opa
     sat6 = sat
     sep7 = sep
     blr8 = blr
     hr9 = hr
    $("#img").css(
        "filter",
        "brightness(" +
            brt +
            ") contrast(" +
            cnt +
            ") grayscale(" +
            gs +
            ") invert(" +
            inv +
            ") opacity(" +
            opa +
            ") saturate(" +
            sat +
            ") sepia(" +
            sep +
            ") blur(" +
            blr +
            "px) hue-rotate(" +
            hr +
            "deg)"
    );
});

function zoom(event) {
    event.preventDefault();
    scale += event.deltaY * -0.01;
    scale = Math.min(Math.max(0.125, scale), 2);
    $("#img").css("transform", "scale(" + scale + ")");
}
let scale = 1;
const el = document.querySelector(".left");
el.onwheel = zoom;


upload.addEventListener('change', e => {
  if (e.target.files.length) {
    const reader = new FileReader();
    reader.onload = e => {
      if (e.target.result) {
        let img = document.createElement('img');
        img.id = 'image';
        img.src = e.target.result;
        result.innerHTML = '';
        result.appendChild(img);
        save.classList.remove('hide');
        options.classList.remove('hide');
        cropper = new Cropper(img);
      }
    };
    reader.readAsDataURL(e.target.files[0]);
  }
});
