---
name: "fmln-tiktok"
description: "Produkcja serii filmów TikTok w Higgsfield dla produktu ze sklepu: hooki, skrypty 20–30 s, klipy image-to-video, lektor PL, montaż 9:16, tryb wolumenu i zwycięzcy, publikacja po akceptacji."
---

# FMLN – klipy z klipu referencyjnego (PDF 3–4 + prompty organic 3, 3b, 3c, 4A)

## Wejście
Przeczytaj ZASADY.md, persona.md i produkt.md z folderu projektu (oraz cel.md, jeśli trwa sprint). Potrzebne: referencja.mp4 (albo link do pobrania przez yt-dlp), produkt_1.jpg (prawdziwe zdjęcie produktu), persona.md. Brak persona.md lub produktu → wróć do skilla fmln-sklep (albo weź produkt z Shopify `search_products` / `get-product`). Brak ZASADY.md → utwórz go wg fmln-sklep, Etap 0.
Narzędzia lokalne: ffmpeg, Pillow, whisper, yt-dlp (doinstaluj brakujące). Jeśli terminal nie może pobrać klipu, poproś o załączenie pliku.

Cel: rozebrać działający klip i zrobić ten sam koncept pod nasz produkt i personę. Klipy 9:16, 15–25 s, pod TikTok, Reels i Facebook Reels, bez nagrywania i bez prawdziwej osoby. Mają wyglądać jak nagrane telefonem przez zwykłą osobę, nie jak reklama. Kopiujemy koncept, nie materiał: zero klatek z referencji, zero cudzych logo i marek.

Gdy nie ma klipu referencyjnego: pomiń krok 1 i pisz skrypt wg struktury PDF 4 (hook 0–3 s bez logo i „cześć”, problem 3–8 s, produkt w akcji 8–18 s, dowód 18–24 s tylko z realną cechą, CTA), z inspiracjami z WinningHuntera (`search_tiktok_videos`, `search_tiktok_ads`, `creative_inspiration_pack`, `get_ad_transcript`). Bierz strukturę, nie treść.

## Psychologia rolki (obowiązuje w każdym skrypcie, wariancie i formacie)
**Hook (0–3 s)** ma wywołać co najmniej jedną reakcję: ciekawość, zaskoczenie, rozpoznanie własnego problemu albo chęć poznania zakończenia. Zaczynaj od wydarzenia, problemu lub intrygującego obrazu, nigdy od przedstawiania produktu. Hook mówiony zawsze razem z mocnym obrazem tego samego (zdanie bez obrazu jest puste). Pierwszy kadr musi być czytelny bez dźwięku.

| Typ hooka | Wzór (dopasuj formę do lektora/lektorki) |
|---|---|
| Curiosity Gap | „Nie wiedziałem/am, że można to zrobić w taki sposób…” |
| Problem | „Najgorsza część [czynności]? Właśnie ta.” + zbliżenie na ten problem |
| Kontrast | „Przez lata robiłem/am to tak, a wystarczyło…” |
| Zaskoczenie | „Myślałem/am, że to kolejny zbędny gadżet.” |
| Historia | „Wszystko zaczęło się od jednej irytującej rzeczy…” |
| Wizualny | Najbardziej nietypowy moment filmu na start, bez wyjaśnienia |

Testowane hooki mają być **różnych typów**, nie kilka wersji tego samego zdania. Przy teście zmienia się tylko pierwsze 2–3 s, reszta klipu identyczna (inaczej nie wiadomo, co zadziałało).

**Open loop:** pokaż problem albo zapowiedz rezultat, rozwiązanie podaj później i domknij przed końcem filmu. Nie przeciągaj sztucznie: jeśli widz czuje, że marnujesz mu czas, technika działa przeciwko nam.

**Retencja:** każda scena robi co najmniej jedno: rozwija historię, daje nową informację, buduje napięcie albo pokazuje istotne działanie. Inaczej wylatuje. Narzędzia: pattern interrupt (zmiana perspektywy, dźwięku, sytuacji), progressive reveal (rozwiązanie po kawałku), visual progression (każde ujęcie wnosi coś nowego), **micro-payoff** (mała, satysfakcjonująca wygrana w połowie klipu, przed finałem), tempo zależne od emocji, rewatch loop (koniec łączy się z początkiem).

**Storytelling:** bohater → problem → napięcie → odkrycie → rozwiązanie → efekt. Ma wyglądać jak sytuacja z życia, nie reklama; najlepiej działa sytuacja, którą odbiorca zna z własnego domu.

**Łańcuch emocji** dobierz do produktu i wpisz do skryptu:
- produkt do domu/sprzątania/naprawy: frustracja → ulga → satysfakcja,
- gadżet/prezent: ciekawość → zaskoczenie → radość,
- inne: wybierz z ciekawość, frustracja, satysfakcja, zaskoczenie, identyfikacja (sytuacja typowa dla persony), kontrast (dwa prawdziwe sposoby obok siebie), dowód społeczny (tylko autentyczna opinia klienta, nigdy wymyślona).

## Krok 1 – Rozbiórka referencji
- ffmpeg: klatki co 1 s, a pierwsze 3 s osobno co 0,25 s w pełnej rozdzielczości. Obejrzyj je dokładnie: hook zdecydował o wyświetleniach.
- Każda scena: ujęcie kamery, co robi ręka, kiedy i jak pojawia się produkt, emocja.
- whisper: czy jest mowa; jeśli tak, spisz sekunda po sekundzie.
- Koncept jednym zdaniem (pokaz bez słów, stare kontra nowe, nieznany problem, recenzja, test, proces z efektem na końcu).
- Wprost: co widać w pierwszej sekundzie i dlaczego człowiek nie przewija.
- Zapisz rozbiorka.md. **STOP: czekaj na „ok”**, bo źle odczytany hook psuje wszystko dalej.

## Krok 2 – Skrypt
Zachowaj strukturę, kolejność scen i długość oryginału; zmień produkt, osobę i język. Słowa z listy języka klienta w persona.md, obietnica realna z persona.md. Trzy wersje pierwszej sceny: każda innego typu hooka (tabela w „Psychologia rolki”), każda pokazuje problem inaczej i w każdej coś się rusza od pierwszej klatki. Przy każdym zdaniu: co jest wtedy na ekranie i jaką emocję z łańcucha ma wywołać. W skrypcie zaznacz: typ każdego hooka, łańcuch emocji, gdzie otwiera się i gdzie domyka open loop, gdzie jest micro-payoff. Scena, która nic nie wnosi (historia, informacja, napięcie, działanie), wylatuje. Polski potoczny, ok. 60–90 słów na 30 s. Zero obietnic zdrowotnych i finansowych, zero wymyślonych opinii i fałszywych „przed i po”. Zapisz skrypt.md.

## Krok 3 – Klatki startowe (Higgsfield)
- Wgraj produkt_1.jpg raz i używaj tego samego pliku jako referencji we wszystkich generacjach.
- Sprawdź koszt jednej klatki i jednego wideo, podaj sumę dla całego planu plus zapas na poprawki (`balance`). **Ruszasz po zgodzie na tę sumę**; w jej granicach dalej bez pytania. Za mało kredytów → powiedz, nie generuj.
- Klatka startowa 9:16 dla każdej sceny. Wspólne zakończenie promptu (po angielsku): ujęcie z iPhone'a, bez retuszu, nic filmowego, bez tekstu, logo i znaku wodnego.
- Ludzie tylko jako dłonie, od tyłu albo od klatki piersiowej w dół; nikt nie mówi do kamery.
- Kontrola przed animacją: w scenach „przed” problem naprawdę widoczny (jeśli wygląda prawie jak „po”, opisz brud lub bałagan dosłownie i mocno, generuj ponownie); produkt ten sam kształt i kolor co na zdjęciu; dłoń ma pięć palców.
- Jeśli Higgsfield zamiast wykonać zlecenie proponuje gotowy preset, odrzuć i ponów to samo zlecenie.
- Alternatywa: jeśli Ads Studio lub Shorts Studio wyraźnie pasuje (`ads_studio_quote`, `shorts_studio_list_presets`), możesz go użyć, ale z tymi samymi zasadami wyglądu produktu i kosztu.

## Krok 4 – Wideo
- Z każdej zaakceptowanej klatki 5 s wideo: Kling 3.0, tryb standardowy, dźwięk wyłączony (`generate_video`, partie przez `generate_video_batch` + `jobs_wait`).
- Trzon promptu: realistyczne nagranie z ręki telefonem, lekkie drganie, bez filmowych ruchów kamery, bez zoomu, bez tekstu i logo.
- Deformacje: produkt w ruchu psuje się po ok. 3 s i gdy zbliża się do kamery. Dopisuj: małe ruchy, jedna ręka, produkt zachowuje kształt, nigdy nie zbliża się do kamery.
- Hook bez ruchu jest martwy: w pierwszej scenie wyraźny ruch od pierwszej klatki.
- Obejrzyj każde wideo co 0,5 s. Jeśli psuje się dopiero w drugiej połowie, nie generuj trzeci raz: weź czyste 2–3 s w montażu. Maks. 2 generacje na scenę. Odrzucone do nieudane/ z jednym zdaniem.
- Odrzuć każdy klip, w którym produkt wygląda inaczej niż w rzeczywistości lub robi coś, czego nie potrafi.

## Krok 5 – Lektor (tylko jeśli koncept ma mowę)
- `list_voices`; jedno krótkie zdanie testowe na dwóch polskich głosach, whisperem sprawdź, który mówi czysto po polsku.
- Po wygenerowaniu całości znów whisper; przekręcone słowo → zmień zapis (np. fonetycznie) i generuj ponownie.
- Lektor mówi nad obrazem, nikt w kadrze nie porusza ustami. Awatar tylko jako prezenter lub narrator, nigdy jako „prawdziwy klient”.

## Krok 6 – Montaż (ffmpeg)
- 1080×1920, 30 kl./s, kolejność ze skrypt.md, cięcia zwykle co 2–4 s, przy lektorze na jego pauzach. Zmieniaj ujęcie wtedy, gdy poprawia to przekaz, nie dlatego, że minął czas; szybsze cięcia przy napięciu i progressive reveal, dłuższe na micro-payoff i efekcie.
- Trzy wersje różniące się tylko pierwszą sceną, każda min. 15 s.
- Napisy w stylu TikToka: 2–3 słowa naraz, duże, białe z grubym czarnym obrysem, pogrubiony font z polskimi znakami; hook większy i od pierwszej klatki. Z lektorem: zsynchronizowane ze słowami (czasy z whispera); bez lektora krótkie zdania ze skryptu na czas sceny.
- Napisy jako przezroczyste PNG (Pillow) nakładane ffmpegiem; za szeroki napis zmniejsz albo złam na dwie linie.
- Wolne 250 px u góry i 450 px u dołu (tam aplikacje zasłaniają obraz). Napisy nigdy na produkcie.
- Bez muzyki (dobiera się w aplikacji przy publikacji). Przy lektorze szczyt ok. −1 dB. Kodowanie H.264 z -preset veryfast.
- Ostatnia klatka łączy się z pierwszą tam, gdzie się da (pętla), bo powtórne oglądanie pomaga zasięgom.

## Krok 7 – Kontrola przed oddaniem
Po 4 klatki z każdego klipu: napis nie zasłania produktu ani dłoni, polskie znaki poprawne, produkt wszędzie taki sam, pierwsza klatka zatrzymuje. Popraw bez pytania.
Checklista psychologii (każde „nie” = popraw przed oddaniem):
1. Czy pierwszy kadr bez dźwięku mówi, o jaki problem/efekt chodzi?
2. Czy film zaczyna się od problemu lub obrazu, a nie od produktu?
3. Czy hooki trzech wersji są różnych typów?
4. Czy open loop domyka się przed końcem i nie jest sztucznie przeciągany?
5. Czy jest micro-payoff przed finałem?
6. Czy każda scena coś wnosi?
7. Czy koniec da się połączyć z początkiem? Opcjonalnie `virality_predictor` do porównania hooków.
Zapisz w gotowe/: koncept_hook1.mp4, koncept_hook2.mp4, koncept_hook3.mp4, skrypt.md, prompty-i-koszt.md (prompty scen, zużyte kredyty, saldo). Raport: co wyszło od razu, co poprawiane i dlaczego, który hook najmocniejszy, co jeszcze warto poprawić. Wyślij klipy użytkownikowi.

## Tryb wolumenu (sprint, dużo klipów tanio)
W organiku wygrywa liczba sensownych prób, nie jeden idealny klip.
- Biblioteka scen: każda udana scena (klatka + czyste sekundy wideo) trafia do sceny/ z opisem w sceny.md. Nowe klipy składaj głównie z istniejących scen; generuj tylko brakujące.
- Macierz hooków: 10 pierwszych scen/zdań (różne typy hooków z PDF 4: pytanie o problem, wynik na start, mit, lista, ciekawość, wskazanie odbiorcy, efekt wizualny) × 2–3 najlepsze środki klipu. Każda kombinacja to nowy klip.
- Tygodniowy cel produkcji z cel.md (np. 14–21 unikalnych klipów). Budżet kredytów na tydzień policz z góry i podaj do akceptacji raz na tydzień.
- Klipy-odpowiedzi: pytania z komentarzy (dostawa, czy działa na X, ile kosztuje) zamieniaj na krótkie klipy z tekstem komentarza na początku, zbudowane z biblioteki scen.
- Każdy klip w trzech wersjach eksportu nie jest potrzebny: jeden czysty plik bez znaku wodnego na wszystkie 3 platformy.

## Tryb zwycięzcy (gdy fmln-raport wskaże klip z wynikiem wyraźnie lepszym niż średnia)
W ciągu 24 h: 5 wariantów tego samego klipu z innym pierwszym zdaniem i inną pierwszą sceną, reszta bez zmian (to ona działała). Dodatkowo 1 klip-odpowiedź na najczęstszy komentarz pod zwycięzcą. Koszt przed generacją.

## Poprawka sceny (gdy użytkownik zgłasza problem)
Użytkownik podaje scenę i co jest nie tak. Porównaj ją z tym samym momentem w referencji (klatki z rozbiorka.md), nazwij czego brakuje, popraw prompt klatki i wideo, podaj koszt, generuj, obejrzyj. Zmontuj klipy ponownie z nową sceną, starą wersję do nieudane/ z notatką. Pokaż starą i nową obok siebie i powiedz, co się zmieniło.

## Kolejne formaty z tych samych scen (materiał na miesiąc)
Dogeneruj tylko brakujące sceny, koszt przed generacją. Każdy format 15–25 s, 9:16:
1. Nieznany problem z lektorem: zaczyna od problemu, którego odbiorca nie zauważa; produkt w połowie.
2. Ciekawość plus cechy z lektorem: produkt w pudełku na początku, „rzecz, o której mało kto wie”. Bez wymyślonych historii o konkurencji czy „zakazanych” informacjach.
3. Prezent (druga persona) jako POV z lektorem innym niż w pozostałych: sytuacja szukania prezentu, wątpliwość, efekt, cena. To scenka, nie recenzja: nie udawaj prawdziwego klienta ani wymyślonych zakupów.
4. Test: stary sposób kontra nasz produkt, ekran dzielony na pół, uczciwy wynik obok siebie na końcu.
5. Storytime na samych napisach: 8–9 krótkich zdań w pierwszej osobie, od frustracji do efektu (jako narracja, bez sugerowania, że to prawdziwa opinia).
6. „Raz za razem”: ten sam efekt kilka razy z rzędu, szybkie cięcia, liczba na końcu.
7. Karuzela 6 zdjęć 9:16: problem, zbliżenie, stary sposób, produkt w akcji, efekt, opakowanie z napisem „Link w opisie”.
Zasady: słowa z języka klienta, jedna rzecz na klip, cena i „link w opisie” na końcu; lektor sprawdzony whisperem słowo po słowie; te same zasady scen co wyżej. Klipy do gotowe/ pod nazwami formatów, karuzela do gotowe/karuzela/, tabela w formaty.md (plik, format, długość, lektor, sceny, tekst). Koszt i saldo. Które dwa formaty wrzucić najpierw i dlaczego.

## Plan publikacji na 30 dni
Na podstawie persona.md, formaty.md i cel.md (jeśli jest):
- Bez sprintu: 1 klip dziennie, od 2. tygodnia 2 dziennie. W sprincie: 2–3 klipy dziennie od pierwszego dnia, ile wymaga cel.md i ile starcza materiału. Ten sam klip tego samego dnia na TikTok, Instagram i Facebook.
- Najpierw trzy wersje pierwszego klipu (test hooka), potem formaty na zmianę; ten sam format nie częściej niż co trzeci dzień (poza wariantami zwycięzcy).
- Różne godziny w kolejnych dniach (rano, południe, wieczór), żeby po tygodniu widać było, co działa; po tygodniu trzymaj się najlepszych pór.
- Do każdego: opis po polsku (1–2 zdania słowami klienta, bez tonu reklamy), 3–5 hashtagów, CTA na zmianę „link w opisie profilu” i „napisz w komentarzu [SŁOWO], wyślę link” (z gotowym szablonem odpowiedzi w wiadomości). W dni bez nowego klipu: ten sam klip z innym pierwszym napisem.
- Za mało klipów: policz brak i zaproponuj, co dorobić (wersje z innym hookiem liczą się jako nowy klip).
- Zapisz plan-publikacji.md (tabela: dzień, godzina, plik, opis, hashtagi, CTA) i plan-publikacji.csv. Daj kroki planowania w Plannerze Meta Business Suite (FB i IG naraz) i w TikTok Studio; muzykę dobiera użytkownik w aplikacji.

## Publikacja na TikTok przez Higgsfield (opcjonalnie)
`tiktok_accounts` (brak konta → `tiktok_connect`). Muzyka tylko dozwolona dla konta firmowego (`tiktok_music_trending` / `tiktok_music_tune`). Opis + hashtagi + CTA; **oznacz treść jako wygenerowaną przez AI** (AI Act art. 50 + etykieta platformy). `tiktok_prepare_publish`, pokaż podgląd i **publikuj tylko po wyraźnym „tak” dla każdego filmu**, nigdy hurtem. Potem `tiktok_publish_status`.

## Log
Dopisz do wyniki.csv w folderze projektu: data, plik, format, hook, typ_hooka, łańcuch_emocji, platforma, link. Z tego korzysta fmln-raport. Po 48 h uzupełnij (jeśli użytkownik poda dane ze statystyk): % widzów po 3 s (ocena hooka), średni czas oglądania i % obejrzeń do końca (retencja), udostępnienia + zapisy (emocja), kliknięcia w link / zamówienia (sprzedaż). Wnioski typu „hook typu Problem trzyma lepiej niż Curiosity Gap” zapisuj w wnioski.md i stosuj w kolejnych skryptach.

## Zakończenie
1–2 zdania: ile klipów gotowych, ile opublikowanych, ile kredytów zużyto i saldo.