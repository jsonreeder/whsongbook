(require 'generic-x)

(defface chord-face
  '((t (:foreground "#FF0000")))
  "red")

(define-generic-mode
  ;; name
  'song-mode
  ;; comment marker
  '("#")
  ;; keywords
  '("title" "artist" "genres" "year" "capo")
  ;; other faces
  '(("header\\|verse\\|chorus\\|bridge\\|instrumental" . 'font-lock-function-name-face)
    ("\\[.+?\\]" . 'chord-face)
    )
  ;; file extension for which to activate this mode
  '("\\.song$")
  ;; other functions to call
  nil
  ;; docstring
  "A mode for song transcriptions"
  )
