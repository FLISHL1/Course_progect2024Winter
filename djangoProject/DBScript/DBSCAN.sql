# CREATE PROCEDURE update_bundle()
# BEGIN
#     INSERT INTO clusters_bundels (type, id, latitude, longitude)
#         SELECT 'F', id, latitude, longitude FROM clusters_food
#             UNION
#         SELECT 'P', id, latitude, longitude FROM clusters_polyclinic;
# end;
#
# CALL update_bundle();
UPDATE clusters_bundels
SET cluster = null
WHERE 1;
DELETE
FROM neighbor
WHERE 1;
/*INSERT INTO cluster_test
SELECT *
FROM clusters_bundels
ORDER BY RAND()
LIMIT 10000;*/
CALL runDBScanTest(0.029, 4);

-- Создаем временную таблицу для хранения кластеров
CREATE INDEX idx_coord ON clusters_bundels (latitude, longitude);

-- Процедура кластеризации DBScan
DELIMITER $$
DROP PROCEDURE runDBScanTest;
CREATE PROCEDURE runDBScanTest(IN eps decimal(5, 3), IN minPts int)
start1:
BEGIN

    DECLARE done INT DEFAULT FALSE;
    DECLARE current_cluster INT DEFAULT 0;
    DECLARE _type VARCHAR(255);
    DECLARE _id INT;
    DECLARE _latitude DECIMAL(19, 17);
    DECLARE _longitude DECIMAL(19, 17);
    DECLARE _type1 VARCHAR(255);
    DECLARE _id1 INT;
    DECLARE _latitude1 DECIMAL(19, 17);
    DECLARE _longitude1 DECIMAL(19, 17);

    DECLARE cur CURSOR FOR SELECT type, id, latitude, longitude FROM clusters_bundels;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    OPEN cur;

    read_loop:
    LOOP
        FETCH cur INTO _type, _id, _latitude, _longitude;
        IF done THEN
            LEAVE read_loop;
        END IF;

        DELETE
        FROM neighbor
        WHERE 1;
        IF (SELECT cluster FROM clusters_bundels WHERE id = _id and type = _type) is null THEN

            INSERT INTO neighbor (type, id, latitude, longitude, cluster)
            SELECT c1.type, c1.id, c1.latitude, c1.longitude, cluster
            FROM clusters_bundels c1
            WHERE ((type, id) != (_type, _id)) and  SQRT(POW(c1.latitude - _latitude, 2) + POW(c1.longitude - _longitude, 2)) <= eps;

            IF (SELECT COUNT(*) FROM neighbor) >= minPts THEN
                SET current_cluster := current_cluster + 1;
                UPDATE clusters_bundels
                SET cluster = current_cluster
                WHERE _type = type
                  and _id = id;

                CREATE TEMPORARY TABLE IF NOT EXISTS individual_neighbor
                (
                    type      VARCHAR(255),
                    id        INT,
                    latitude  DECIMAL(19, 17),
                    longitude DECIMAL(19, 17),
                    cluster   int,
                    PRIMARY KEY (type, id)
                );

                DELETE
                FROM individual_neighbor
                WHERE 1;

                DELETE
                FROM neighbor
                WHERE cluster is not null;

                while EXISTS(SELECT 1 FROM neighbor)
                    Do
                        SELECT type, id, latitude, longitude
                        INTO _type1, _id1, _latitude1, _longitude1
                        FROM neighbor
                        WHERE cluster is null
                        ORDER BY RAND()
                        LIMIT 1;

                        INSERT INTO individual_neighbor (type, id, latitude, longitude, cluster)
                        SELECT c1.type, c1.id, c1.latitude, c1.longitude, c1.cluster
                        FROM clusters_bundels c1
                        WHERE ((type, id) != (_type1, _id1)) and  SQRT(POW(c1.latitude - _latitude1, 2) + POW(c1.longitude - _longitude1, 2)) <=
                              eps;

                        IF (SELECT COUNT(*) FROM individual_neighbor) >= minPts THEN

                            INSERT INTO neighbor (type, id, latitude, longitude, cluster)
                            SELECT c1.type, c1.id, c1.latitude, c1.longitude, c1.cluster
                            FROM individual_neighbor c1
                                     LEFT JOIN neighbor c2 ON c1.id = c2.id and c1.type = c2.type
                            WHERE c2.id is null
                              and c1.cluster is null;
                        end if;

                        UPDATE clusters_bundels
                        SET cluster = current_cluster
                        WHERE _type1 = type
                          and _id1 = id;

                        DELETE
                        FROM individual_neighbor
                        WHERE 1;

                        DELETE
                        FROM neighbor
                        WHERE (type = _type1
                            and id = _id1)
                           or cluster is not null;


                    end while;
                DROP TEMPORARY TABLE individual_neighbor;

            END IF;
            DELETE
            FROM neighbor
            WHERE 1;

        end if;

    END LOOP;

    CLOSE cur;
END
$$

DELIMITER ;

# CREATE TEMPORARY TABLE outsiders
# (
#     type      VARCHAR(255),
#     id        INT,
#     latitude  DOUBLE,
#     longitude DOUBLE,
#     PRIMARY KEY (type, id)
# );
/*DROP PROCEDURE iterator;
CREATE PROCEDURE iterator(IN _type VARCHAR(255), IN _id int, IN _latitude DOUBLE, IN _longitude DOUBLE,
                          IN eps decimal(5, 3), IN minPts int, IN current_cluster int)
BEGIN
    DECLARE done1 INT DEFAULT FALSE;
    DECLARE cur CURSOR FOR SELECT n1.type, n1.id, n1.latitude, n1.longitude
                           FROM neighbor n1
                           WHERE n1.type != _type
                             and n1.id != _id;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done1 = TRUE;
#     CREATE INDEX idx_coord1 ON clone_neighbor (type, id);

    INSERT INTO neighbor (type, id, latitude, longitude)
    SELECT DISTINCT c1.type, c1.id, c1.latitude, c1.longitude
    FROM cluster_test c1
    WHERE c1.cluster is null
      AND SQRT(POW(c1.latitude - _latitude, 2) + POW(c1.longitude - _longitude, 2)) <= eps;

    IF (SELECT COUNT(*) FROM neighbor) >= minPts THEN
        -- Обновляем кластер для найденных соседей

        UPDATE cluster_test
        SET cluster = current_cluster
        WHERE _type = type
          and _id = id;

        OPEN cur;
        loop_neighbor:
        LOOP
            FETCH cur INTO _type, _id, _latitude, _longitude;
            IF done1 THEN
                LEAVE loop_neighbor;
            END IF;

            DELETE
            FROM neighbor
            WHERE 1;

            CALL iterator(_type, _id, _latitude, _longitude, eps, minPts, current_cluster);
        end loop;
        CLOSE CUR;
        -- Убираем точки из временной таблицы, так как они не образуют кластер
    else
        UPDATE cluster_test
        SET cluster = current_cluster
        WHERE _type = type
          and _id = id;
        #         INSERT INTO outsiders(type, id, latitude, longitude)
#             VALUES
    END IF;

end;*/
CREATE INDEX idx_coord1 ON temp_clusters (latitude, longitude);

DELETE
FROM neighbor
WHERE 1;
-- Задаем параметры DBScan
CREATE TABLE neighbor
(
    type      VARCHAR(255),
    id        INT,
    latitude  DOUBLE,
    longitude DOUBLE,
    cluster   int,
    PRIMARY KEY (type, id)
);

-- Минимальное количество точек в окрестности

-- Запускаем процедуру
CALL runDBScanTest(0.09, 4);

SET max_sp_recursion_depth = 255;
SELECT SQRT(POW(55.49835 - 55.41741, 2) + POW(36.92442 - 36.87060, 2));







SELECT c1.type, c1.id, c1.latitude, c1.longitude, cluster
            FROM cluster_test c1
            WHERE ((type, id) != ('F', 19367)) and  SQRT(POW(c1.latitude - 55.66917, 2) + POW(c1.longitude - 37.44756, 2)) <= 0.025;