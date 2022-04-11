using Microsoft.AspNetCore.Mvc;
using MySqlConnector;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Newtonsoft.Json;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace FurnitureStore.Controllers {
    [Route("api/[controller]")]
    [ApiController]
    public class SpendingHabits : ControllerBase {
        // GET: api/<SpendingHabits>
        [HttpGet]

        public string Get() {
            using var connection = new MySqlConnection(Globals.connString);
            connection.Open();

            string query =  @"SELECT R.Region_Name, SUM(Z.Totale2) as Totale3
                            FROM Regions R, Provinces P, Municipalities M, (
	                            SELECT M.Municipality_Id, SUM(Y.Totale1) as Totale2 
	                            FROM Municipalities M, (
		                            SELECT X.Card_Id, X.Municipality_Id, SUM(X.Total) as Totale1
                                    FROM (SELECT DISTINCT C.Card_Id, C.Municipality_Id, T.Transaction_Id, T.Total FROM Cards C, Transactions T 
                                        WHERE C.Card_Id = T.Card_Id AND T.Total != 0) X 
                                    GROUP BY X.Card_Id) Y
	                            WHERE M.Municipality_Id = Y.Municipality_Id
	                            GROUP BY M.Municipality_Id) Z
                            WHERE P.Region_Id = R.Region_Id AND M.Province_Id = P.Province_Id AND M.Municipality_Id = Z.Municipality_Id
                            GROUP BY R.Region_Id;";
            var command = new MySqlCommand(query, connection);
            using var reader = command.ExecuteReader();
            var res = new List<RegionalSpending>();
            while (reader.Read()) {
                var ciao = (string)reader.GetValue(0);
                var ciaone = (double)reader.GetValue(1);
                res.Add(new RegionalSpending {RegionName = ciao, TotalSpent = ciaone});
            }
            var dioxcan = JsonConvert.SerializeObject(res);
            connection.Close();
            return dioxcan;
        }

        // GET api/<SpendingHabits>/5
        [HttpGet("{id}")]
        public string Get(int id) {
            using var connection = new MySqlConnection(Globals.connString);
            connection.Open();

            string query = string.Format(   @"SELECT P.Province_Name, SUM(Z.Totale2) as Totale3
                                            FROM Provinces P, Municipalities M, (
	                                            SELECT M.Municipality_Id, SUM(Y.Totale1) as Totale2 
	                                            FROM Municipalities M, (
		                                            SELECT X.Card_Id, X.Municipality_Id, SUM(X.Total) as Totale1
                                                    FROM (SELECT DISTINCT C.Card_Id, C.Municipality_Id, T.Transaction_Id, T.Total FROM Cards C, Transactions T 
                                                        WHERE C.Card_Id = T.Card_Id AND T.Total != 0) X 
                                                    GROUP BY X.Card_Id) Y
	                                            WHERE M.Municipality_Id = Y.Municipality_Id
	                                            GROUP BY M.Municipality_Id) Z
                                            WHERE P.Region_Id = {0} AND M.Province_Id = P.Province_Id AND M.Municipality_Id = Z.Municipality_Id
                                            GROUP BY P.Province_Id", id);
            var command = new MySqlCommand(query, connection);
            using var reader = command.ExecuteReader();
            var res = new List<ProvinceSpending>();
            while (reader.Read()) {
                var ciao = (string)reader.GetValue(0);
                var ciaone = (double)reader.GetValue(1);
                res.Add(new ProvinceSpending { ProvinceName = ciao, TotalSpent = ciaone });
            }
            var dioxcan = JsonConvert.SerializeObject(res);
            connection.Close();
            return dioxcan; ;
        }

    }
}
