using Microsoft.AspNetCore.Mvc;
using MySqlConnector;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace FurnitureStore.Controllers {
    [Route("api/[controller]")]
    [ApiController]
    public class CardsController : Controller {
        [HttpGet]
        public string Get() {
            using var connection = new MySqlConnection(Globals.connString);
            connection.Open();

            string query = "SELECT C.Card_Id, C.Birthday FROM Cards C";

            var command = new MySqlCommand(query, connection);
            using var reader = command.ExecuteReader();
            var res = new List<Ages>();
            res.Add(new Ages { age_range = "18-25", counter = 0 });
            res.Add(new Ages { age_range = "26-35", counter = 0 });
            res.Add(new Ages { age_range = "36-45", counter = 0 });
            res.Add(new Ages { age_range = "46-55", counter = 0 });
            res.Add(new Ages { age_range = "56-65", counter = 0 });
            res.Add(new Ages { age_range = "65+", counter = 0 });

            var today = DateTime.Today;

            var a = (today.Year * 100 + today.Month) * 100 + today.Day;

            while (reader.Read()) {
                var ciao = (int)reader.GetValue(0);
                var ciaone = (DateTime)reader.GetValue(1);

                var b = (ciaone.Year * 100 + ciaone.Month) * 100 + ciaone.Day;

                var c = (a - b) / 10000;

                if (c >= 18 && c <= 25) {
                    res[0].counter++;
                }
                else if (c >= 26 && c <= 35) {
                    res[1].counter++;
                }
                else if (c >= 36 && c <= 45) {
                    res[2].counter++;
                }
                else if (c >= 46 && c <= 55) {
                    res[3].counter++;
                }
                else if (c >= 56 && c <= 65) {
                    res[4].counter++;
                }
                else if (c > 65) {
                    res[5].counter++;
                }

            }
            var dioxcan = JsonConvert.SerializeObject(res);
            connection.Close();
            return dioxcan;
        }

    }
}
