;; song-mode. song-mode, a major mode for transcribing songs

(setq my-highlights
      '(("title:\\|artist:\\|recorded:\\|genre:\\|capo:" . font-lock-function-name-face)
        ("(Chorus)" . font-lock-constant-face)))

(define-derived-mode song-mode fundamental-mode
  (setq font-lock-defaults '(my-highlights))
  (setq mode-name "Song"))
