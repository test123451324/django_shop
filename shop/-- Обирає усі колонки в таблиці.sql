-- Обирає усі колонки в таблиці
-- SELECT * FROM shop_product;
-- SELECT name,price FROM shop_product
-- Шукає в тексті щоб була r
-- WHERE name LIKE '%r%'
-- Шукає щоб слова закінчувались на r
-- WHERE name LIKE '%r';
-- WHERE price>100;
-- Сортування від більшого до меншого
-- ORDER BY rate DESC
-- Сортування від меншого до більшого
-- ORDER BY rate
-- LIMIT 3;
-- SELECT COUNT(*) FROM shop_product WHERE price>100;
-- SELECT
--  COUNT(*) AS total,
--  AVG(price) AS avg_price,
--  MAX(price) AS max_price,
--  MIN(price) AS min_price
-- FROM shop_product;
SELECT
--  shop_product.name AS product_name,
 shop_category.name AS category_name,
 AVG(shop_product.price) AS avg_price
--  COUNT(shop_product.id) AS product_count
 
FROM shop_product
JOIN shop_category
ON shop_product.category_id=shop_category.id
-- WHERE shop_category.name="Drink"
GROUP BY shop_category.name;