--create schema student_project;

select *
from student_project.properties_cleaned pc 

 

--1 Average,lowest and highest list price by property type

select property_type,
count(*)as total_properties,
Round(Avg("list_price")::numeric,2)as avg_price,
round(percentile_cont(0.5)within group (order by list_price)::numeric,2)as median_price,
Min("list_price") as Lowest_price,
Max("list_price") as Highest_price
from student_project.properties_cleaned
group by property_type
order by avg_price desc; 


--2 average square footage and price per square feet by property type (Land has no sqft,so leave it out)
select "property_type",
round(avg("property_sqft")::numeric,2)as Avg_list_sqft,
round(avg("price_per_sqft")::numeric,2)as Avg_price_per_sqft,
count(*)as Total_listing
from student_project.properties_cleaned pc 
where pc.property_sqft > 0
group by "property_type"
order by avg_price_per_sqft DESC ;

--3  price reduction amount by property type?

select "property_type",
round(avg("amount_reduced")::numeric,2)as avg_amt_reduce,
count(*) filter (where amount_reduced >0) as Listings_with_reductions,
count(*)as total_listings
from student_project.properties_cleaned pc 
group by "property_type"
order by avg_amt_reduce desc;

--4 minimum,maximum,and average list price by property type ?
select "property_type",
round(MIN("list_price")::numeric,2)as min_price,
round(max("list_price")::numeric,2)as max_price,
round(avg("list_price")::numeric,2)as avg_price,
count(*)as Total_listing
from student_project.properties_cleaned pc 
group by "property_type"
order by max_price desc;

--5  price by number of bedrooms ?
select "property_type",
"bedrooms",
count(*) as total_listing,
round(avg("list_price")::numeric,2)as avg_price
from student_project.properties_cleaned pc 
where"bedrooms" > 0
group by property_type,bedrooms
order by property_type,bedrooms asc ;

--6  percentage of listing with a reduced prices ?
select "property_type",
count(*)as total_listing,
count(*)filter (where amount_reduced >0) as listing_with_discount,
round(100.0*count(*)filter(where amount_reduced > 0)/count(*),2)pct_with_discount
from student_project.properties_cleaned pc
group by "property_type"
order by pct_with_discount desc;

--7 Market Segmentation into custom prices per
--How are properties distributed across realistic LA price tiers

select 
case
	when "list_price"< 750000 then '1. Entry Level (< $750k)'
	when "list_price" < 1500000 then '2. Mid-Range (750K- 1.5M)'
	when "list_price" < 3500000 then '3. High-end (1.5M-3.5M)'
	when "list_price"< 5000000 then '4.Luxury (3.5M-5M)'
	else                            '5.Ultra-Luxury (5M+)'
	end  as price_tier,
count(*) as total_properties,
Round(avg("list_price")::numeric,2)as avg_tier_price,
round(avg("property_sqft")::numeric,0) as avg_sqft
from student_project.properties_cleaned pc 
group by price_tier 
order by price_tier asc ;

--- 8. type whose average price is above the overall average

with overall as (
select Avg("list_price")as overall_city_avg
from student_project.properties_cleaned)

select property_type as property_category,
count(*)as total_listing,
round(avg("list_price")::numeric,2) as category_avg_price
from student_project.properties_cleaned
group by property_type
having count(*) >= 5 
and  avg ("list_price")>(select overall_city_avg from overall)
order by category_avg_price desc

--9) top 3 most expensive listing per type ?

with Ranked as (select property_type,bedrooms,property_sqft,list_price,
rank () over(partition by property_type order by list_price desc ) as price_rank
from student_project.properties_cleaned)
select property_type,price_rank,bedrooms,property_sqft,
list_price
from Ranked
where price_rank <= 3
order by property_type,price_rank

---10) Each listing versus its categroy average
select property_type,bedrooms,property_sqft,list_price,
round(avg(list_price) over (partition by property_type)::numeric,2) as avg_category_price,
round((list_price - avg(list_price)over(partition by property_type))::numeric,2)as variance_from_avg
from student_project.properties_cleaned
order by variance_from_avg


