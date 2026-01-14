let app = Sys.getcwd () |> String.split_on_char '/' |> List.rev |> List.hd
(* let app = "cs134b" *)
let title = "GNU Dynamic Language Runtime"
let about = "
- minimal dynamic language runtime
- written in Rust
"

(* *)
let user = "dponyatov"
let ruser = "dimon"
let devserver = "10.110.1.101"

(* *)
let author = "Dmitry Ponyatov"
let email = "dponyatov@gmail.com"
let year = 2026
let version = "0.0.1"
let license = "MIT"
let github = [%string "https://github.com/ponyatov/%{app}"]
let gitflic = [% string "https://gitflic.ru/project/%{user}/%{app}"]
