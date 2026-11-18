create schema student_project;

select *
from student_project.properties_cleaned pc 

 

--1 Which property type has the highest average list price in los Angeles ?

select
count(*)as total_properties,
Round(Avg("List_price")::numeric,2)as overall_avg_price,
Round(Min("List_price")::numeric,2)as Lowest_price,
Round(Max("List_price")::numeric,2)as Highest_price
from student_project.properties_cleaned



--2 What is the average square footage and price per square feet by property type?
select "Property_type",
round(avg("Property_sqft")::numeric,2)as Avg_list_sqft,
round(avg("Price_per_sqft")::numeric,2)as Avg_price_per_sqft,
count(*)as Total_listing
from student_project.properties_cleaned pc 
group by "Property_type"
order by avg_price_per_sqft DESC ;

--3 what is the average price reduction amount by property type?

select "Property_type",
round(avg("Amount_reduced")::numeric,2)as avg_amt_reduce,
count(case when "Amount_reduced" > 0 then 1 end)as Listings_with_reductions,
count(*)as total_listings
from student_project.properties_cleaned pc 
group by "Property_type"
order by avg_amt_reduce desc;

--4 what are the minimum,maximum,and average list price by property type ?
select "Property_type",
round(MIN("List_price")::numeric,2)as min_price,
round(max("List_price")::numeric,2)as max_price,
round(avg("List_price")::numeric,2)as avg_price,
count(*)as Total_listing
from student_project.properties_cleaned pc 
group by "Property_type"
order by max_price desc;

--5 How does price change as the number of bedrooms increases?
select "Property_type",
"Bedrooms",
count(*) as total_listing,
round(avg("List_price")::numeric,2)as avg_price
from student_project.properties_cleaned pc 
where"Bedrooms" > 0
group by "Property_type","Bedrooms"
order by "Property_type","Bedrooms" asc ;

--6 What percentage of properties in each property type have reduced prices ?
select "Property_type",
count(*)as total_listing,
count(case when "Amount_reduced">0 then 1 end)as listing_with_discount,
round((count(case when "Amount_reduced">0 then 1 end)::numeric/count(*)::numeric)*100,2)as pct_with_discount
from student_project.properties_cleaned pc
group by "Property_type"
order by pct_with_discount desc;

--7 Market Segmentation into custom prices per
--How are properties distributed across realistic LA price tiers

select 
case
	when "List_price"< 750000 then '1. Entry Level'
	when "List_price" between 750000 and 1500000 then '2. Mid-Range'
	when "List_price" between 1500001 and 3500000 then '3. High-end'
	else '4.Over $5m (Ultra-Luxury)'
	end  as price_tier,
count(*) as total_properties,
Round(avg("List_price")::numeric,2)as avg_tier_price,
round(avg("Property_sqft")::numeric,0) as avg_sqft
from student_project.properties_cleaned pc 
group by price_tier 
order by price_tier asc ;

--- 8. Which major property type have an average list price above the overall market value

with overallmarket as (
select Avg("List_price")as overall_city_avg
from student_project.properties_cleaned)
select
"Property_type" as property_category,
count(*)as total_listing,
round(avg("List_price")::numeric,2) as category_avg_price
from student_project.properties_cleaned
group by property_category
having count(*) >= 5 
and  avg ("List_price")>(select overall_city_avg from overallmarket);

--9) what are the top 3 most expensive properties within each property type?
with Ranked_listings as (
select "Property_type",
"Bedrooms",
"Property_sqft",
"List_price",
rank () over(
partition by "property_type"
order by "List_price" desc ) as price_rank
from student_project.properties_cleaned)
select
"Property_type",
price_rank,
"Bedrooms",
"Property_sqft",
"List_price"
from Ranked_listings
where price_rank <= 3
order by "Property_type" asc,
price_rank asc

---10) How does each property's list price campare to its category average ? 

with category_average as(
select "Property_type",
round(avg("List_price")::numeric,2)as avg_category_price
from student_project.properties_cleaned
group by "Property_type")

select pc."Property_type",
pc."Bedrooms",
pc."Property_sqft",
pc."List_price",
ca.avg_category_price,
round((pc."List_price"-ca.avg_category_price)::numeric,2)as variance_from_avg
from student_project.properties_cleaned pc 
join category_average ca
on pc."Property_type"=ca."Property_type"
order by variance_from_avg desc;










