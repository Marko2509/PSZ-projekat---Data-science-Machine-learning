# 46 zapisa imalo je menjac='Automatski' i jedan zapis je imao menjac='Poluautomatski' -> promenjeno u Automatski/Poluautomatski menjac
# obrisani duplikati

select lokacija, count(*) as 'broj automobila'
from cars_table
group by lokacija
order by count(*) desc
limit 10;

select c.opseg as 'opseg kilometraze', count(*) 'broj automobila'
from (
  select case  
	when kilometraza between     0  and 49999  then '1. ispod 50 000'
	when kilometraza between 50000  and 99999  then '2. 50 000 - 99 999'
	when kilometraza between 100000 and 149999 then '3. 100 000 - 149 999'
	when kilometraza between 150000 and 199999 then '4. 150 000 - 199 999'
	when kilometraza between 200000 and 249999 then '5. 200 000 - 249 999'
	when kilometraza between 250000 and 299999 then '6. 250 000 - 299 999'
	else '7. 300000+' 
  end as opseg
  from cars_table) as c
group by c.opseg
order by c.opseg;

select c.opseg as 'opseg godista', count(*) 'broj automobila'
from (
  select case  
	when godiste               <= 1960 then '1960. i starije'
	when godiste between 1961 and 1970 then '1961-1970'
	when godiste between 1971 and 1980 then '1971-1980'
	when godiste between 1981 and 1990 then '1981-1990'
	when godiste between 1991 and 2000 then '1991-2000'
	when godiste between 2001 and 2005 then '2001-2005'
    when godiste between 2006 and 2010 then '2006-2010'
    when godiste between 2011 and 2015 then '2011-2015'
    when godiste between 2016 and 2020 then '2016-2020'
	else '2021-2022'
  end as opseg
  from cars_table) as c
group by c.opseg
order by c.opseg;

select c.menjac, count(*) as 'broj automobila', count(*) / tmp.cnt * 100 as 'procenat svih automobila'
from cars_table c
cross join (select count(*) as cnt from cars_table) tmp
group by c.menjac, tmp.cnt;

select c.opseg as 'opseg cena', count(*) 'broj automobila', count(*) / tmp.cnt * 100 as 'procenat svih automobila'
from (
  select case  
	when cena                  < 2000 then '1.  0 -  1 999e'
	when cena between  2000 and  4999 then '2.  2 000 -  4 999e'
	when cena between  5000 and  9999 then '3.  5 000 -  9 999e'
	when cena between 10000 and 14999 then '4. 10 000 - 14 999e'
	when cena between 15000 and 19999 then '5. 15 000 - 19 999e'
	when cena between 20000 and 24999 then '6. 20 000 - 24 999e'
    when cena between 25000 and 29999 then '7. 25 000 - 29 999e'
	else '8. 30 000e+'
  end as opseg
  from cars_table) as c cross join (select count(*) as cnt from cars_table) tmp
group by c.opseg, tmp.cnt
order by c.opseg;