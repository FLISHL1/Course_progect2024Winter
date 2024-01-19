create definer = user@`%` procedure update_bundle()
BEGIN
    INSERT INTO clusters_bundels (type, id, latitude, longitude)
        SELECT 'F', id, latitude, longitude FROM clusters_food
            UNION
        SELECT 'P', id, latitude, longitude FROM clusters_polyclinic;
end;





create definer = user@`%` procedure runDBScanTest(IN eps decimal(8,7), IN minPts int)
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
    UPDATE clusters_bundels
    SET cluster = null
    WHERE 1;
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
END;

