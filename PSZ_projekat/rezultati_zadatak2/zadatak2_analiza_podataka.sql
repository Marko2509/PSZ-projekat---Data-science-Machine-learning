# obrisani svi redovi sa null cenama i cenama na upit/po dogovoru
# kolone kilometraza, kubikaza i cena kastovane u int
# ostavio snagu motora u kW i kastovao u int
# id 6891 ima null za broj_vrata postavio 4/5 (rucni uvid u oglas)
# id 19478 ima marku 'Ostalo' (u pitanju je neki egzoticni old-tajmer) i nema model -> nije od interesa za nas projekat pa je obrisan
# id 4284 ima gorivo null -> zakljucujemo da je dizel jer se vidi iz naziva oglasa da je d4
# id 13545 ima ostecenje null -> brisemo red jer je bitan podatak, a ne mozemo ga pogoditi
# id 23642 ima klima null -> postavljamo na automatska kao rezultat poredjenja sa istim modelima
# sredjeni nerealno veliki iznosi za kilometrazu i kubikazu
# ispravljen automobil koji nije imao marku, ali je imao model Golf4

select marka, count(*) as 'broj automobila' 
from cars_table
group by marka;

select lokacija, count(*) as 'broj automobila' 
from cars_table
group by lokacija;

select boja, count(*) as 'broj automobila' 
from cars_table
group by boja;

select *
from cars_table
order by cena desc
limit 30;

select *
from cars_table
where karoserija = 'Džip/SUV'
order by cena desc
limit 30;

select *
from cars_table
where godiste = 2021 or godiste = 2022
order by cena desc;

SELECT *
FROM cars_table
where kubikaza is not null
order by kubikaza desc
limit 1;

SELECT *
FROM cars_table
order by snaga_motora desc
limit 1;

SELECT *
FROM cars_table
order by kilometraza desc
limit 1;