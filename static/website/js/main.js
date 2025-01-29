document.addEventListener("DOMContentLoaded", _ => {


    setTimeout(() =>document.getElementById("loader").style.display = "none", 300);

    document.addEventListener("scroll", (e) => {
        if (scrollY > 200) {
            document.querySelector("#nav").classList.add("shadow")
        } else {
            document.querySelector("#nav").classList.remove("shadow")
        }
    });

    const toggle = () => document.querySelector("#menu-navigation").classList.toggle("hidden");
    document.querySelector("#menu-navigation-btn").addEventListener("click", (e) => toggle());
});

const HidePopUp = () => document.querySelector("#popup").classList.add("hidden");