SELECT
  customer_id,
  COUNT(product_id) AS number_of_products_viewed
FROM
  product_views
WHERE
  customer_id = '1234567890'
AND
  date_created BETWEEN '2023-01-01' AND '2023-12-31'
GROUP BY
  customer_id
ORDER BY
  number_of_products_viewed DESC
