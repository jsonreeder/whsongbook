(require 'generic-x)

(defface chorus-face
  '((t (:foreground "#FF0000")))
  "red")

(define-generic-mode 
  ;; name
  'song-mode
  ;; comment marker
  '("#")
  ;; keywords
  '("title" "artist" "genre" "year" "capo" "streudel")
  ;; other faces
  '(("(Chorus)" . 'font-lock-function-name-face)
    ("|\\|:" . 'font-lock-builtin-face)
    ("^\s\s\s\s[A-Za-z].*" . 'chorus-face))
  ;; file extension for which to activate this mode 
  '("\\.song$")
  ;; other functions to call
  nil
  ;; docstring
  "A mode for song transcriptions"
  )
