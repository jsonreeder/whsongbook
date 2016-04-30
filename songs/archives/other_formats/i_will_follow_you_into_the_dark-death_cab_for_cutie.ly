\header {
  title = "I Will Follow You Into the Dark"
  composer = "Death Cab for Cutie"
}

\new ChordNames \with {
  \override BarLine #'bar-extent = #'(-2 . 2)
  \consists "Bar_engraver"
}

\chordmode {
  \transpose c c { % Change second note to transpose piece
    % Text alignment
    \override Score.RehearsalMark #'break-align-symbol = #'(key-signature)
    \override Score.RehearsalMark #'self-alignment-X = #-1
    
    % Chords
    \mark "Chorus"
      a1:m c f c2 g
      a1:m c g g \break
      a:m c e a2:m g
      f1 f:m c c \break

    \bar "||" \break

    \mark "Verse"
      c1 a:m f c2 g
      c1 a:m f c2 g \break
    \bar "|."
  }

}

% Lyrics
\markup {
  \vspace #3.0 % Space between chords and lyrics
  \huge { % \teeny \tiny \small \normalsize \large \huge
    \fill-line {
      \column {
       "Love of mine some day you will die"
       "But I'll be close behind. I'll follow you into the dark,"
       "No blinding light or tunnels to gates of white"
       "Just our hands clasped so tight, waiting for the hint of a spark."

        \hspace #1.0 % Space between verses
        "If Heaven and Hell decide that they both are satisfied"
        "Illuminate the 'no's on their vacancy signs"
        "If there's no one beside you when your soul embarks"
        "Then I'll follow you into the dark"

        \hspace #1.0 % Space between verses
        "In Catholic school as vicious as Roman rule"
        "I got my knuckles bruised by a lady in black"
        "And I held my tongue as she told me"
        "\"Son, fear is the heart of love.\" So I never went back"
        
        \hspace #1.0 % Space between verses
        "[Chorus]"
       
       \hspace #1.0 % Space between verses
        "You and me have seen everything to see"
       "From Bangkok to Calgary, and the soles of your shoes "
       "Are all worn down. The time for sleep is now."
       "It's nothing to cry about, 'cause we'll hold each other soon"
       "In the blackest of rooms"

\hspace #1.0 % Space between verses
        "[Chorus]"
        "…and I’ll follow you into the dark."
      }
    }
  }
}

\version "2.16"  % necessary for upgrading to future LilyPond versions.