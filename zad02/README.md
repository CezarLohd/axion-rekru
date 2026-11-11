# ZADANIE 2 #

Cezary Kalarus <br><br>
Symulator w pliku [zad02.py](zad02.py)
<br>
# NOTATKA #
Wydaję mi się, że wszystko zrozumiałem z tego co było na wykładzie. Natomiast na samym wykładzie mało było o bramce $R_y$ (chyba że irl było coś więcej dopowiedziane, czego w pdfie samym nie było, to shame on me). Zresztą nawet żeby samemu zaimplementować to w symulatorze potrzebowałem to wyszukać, więc na jej temat się troszkę bardziej dodoktoryzowałem. 

### Na początku musiałem znaleźć wartości jakie powinna mieć jej macierz. ###
Jest to oczywiście:

$$
R_y(\theta) = 
\begin{bmatrix} 
\cos(\frac\theta 2) & -\sin(\frac\theta 2) \\ 
\sin(\frac\theta 2) & \cos(\frac\theta 2) 
\end{bmatrix}
$$

Może nasunąć się pytanie: skąd w ogóle tu te funkcje trygonometryczne? 

Gdy mamy punkt na zwykłym okręgu w układzie współrzędnych to jego $x = R \cdot \cos\theta$, a $y = R \cdot \sin\theta$, gdzie R to oczywiście promień (u nas = 1) a $\theta$ to kąt między osią OX a przedłużeniem promienia przecinającym tą oś i przechodzącym przez właśnie ten punkt.

Tak samo będzie dla liczby zespolonej ($z = \alpha + i\beta $), gdzie $\alpha$ i $\beta$ to będą właśnie te same współrzędne, odpowiednio x i y, R będzie $|z| = 1$, a $\theta$ argumentem głównym $Arg(z)$. Widzimy z tej analogii że $\alpha = \cos\theta$ oraz $\beta = \sin\theta$.

A jak obrócić taką liczbę? Weźmy kąt $\phi$. Chcąc obrócić liczbę zespoloną o ten kąt (na wykresie zespolonym), mnoży się ją przez $e^{i\phi} = \cos\phi + i\sin\phi$. Mamy wtedy: 

$$
z_2 = (\alpha + i\beta) \cdot (\cos\phi + i\sin\phi) \\
z_2= \alpha\cos\phi + i\beta\cos\phi + i\alpha\sin\phi + \underbrace{i^2}_{-1} \cdot \beta\sin\phi \\
z_2 = \underbrace {\alpha\cos\phi - \beta\sin\phi}_{\text{cz. rzeczywista - nowe } \alpha_2} + i\underbrace{(\beta\cos\phi + \alpha\sin\phi)}_{\text{cz. urojona - nowe }\beta_2}
$$

#### Jak to się ma do naszej bramki? ####

Spójrzmy teraz na macierz obrotu $R(\phi)$
przemnożoną z wektorem kubitu:

$$
\begin{bmatrix}
\cos\phi & -\sin\phi \\ 
\sin\phi & \cos\phi 
\end{bmatrix}
\begin{bmatrix} 
\alpha \\ 
\beta 
\end{bmatrix}
=
\begin{bmatrix} 
\alpha\cos\phi - \beta\sin\phi \\ 
\alpha\sin\phi + \beta\cos\phi 
\end{bmatrix}
$$

Górny wiersz stanu wynikowego to właśnie cz. rzeczywista $Re(z_2)$, a dolny wiersz to cz. urojona $Im(z_2)$.

Co oznacza, że w zasadzie mnożenie wektora przez tą macierz $R(\phi)$ robi dokładnie to samo co przemnożenie liczby zespolonej przez $e^{i\phi}$ - obraca punkt po okręgu o $\phi$ stopni.

### Teraz tylko pytanie, skąd w naszej macierzy $R_y(\theta)$ wszechobecny kąt $\frac\theta 2$ a nie poporstu $\theta$?
Nasza macierz obrotu to dokładnie $R_y(\theta)$, tylko z podstawionym $\phi = \frac\theta 2$. Na sferze Blocha, kątem $\theta$ oznaczamy kąt jakim obracamy stan na kuli. <br>
Na tej sferze też stany przeciwne: |0> - biegun północny i |1> - biegun południowy, leżą naprzeciwko siebie - w odległości 180 stopni $ = \theta$. <br>
W naszym układzie (dwuwymiarowym) wektorów stan |0> $=\begin{bmatrix}1 \\ 0\end{bmatrix} $ leży na osi poziomej, a stan |1> = $=\begin{bmatrix}0 \\ 1\end{bmatrix} $ leży na osi pionowej. Dzieli je kąt prosty $\frac\pi 2$. <br>
W takim razie, skoro przejście ze stanu |0> na |1> na Sferze Blocha 180 st. a na dwuwym. układzie połowę tego - 90 st. to kąt wektora $\phi$ musi być 2 razy mniejszy od kąta na sferze $\theta$: $\phi = \frac\theta 2$. <br>
Dlatego właśnie w ciele wzoru na bramkę $R_y(\theta)$ występuje kąt $\frac\theta 2$ a cała bramka to poprostu obrót
po okręgu jednostkowym o połowę kąta ze Sfery Blocha.

---
---
Źródło wiedzy: https://en.wikipedia.org/wiki/List_of_quantum_logic_gates#Rotation_operator_gates

---
---