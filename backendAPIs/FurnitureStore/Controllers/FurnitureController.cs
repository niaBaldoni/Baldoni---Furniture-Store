using Microsoft.AspNetCore.Mvc;
using MySqlConnector;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Microsoft.AspNetCore.Cors;

// For more information on enabling Web API for empty projects, visit https://go.microsoft.com/fwlink/?LinkID=397860

namespace FurnitureStore.Controllers {
    [Route("api/[controller]")]
    [ApiController]
    public class FurnitureController : ControllerBase {

        // GET: api/<FurnitureController>
        [HttpGet]
        public IEnumerable<string> Get() {
            return new string[] { "value1", "value2" };
        }

        // GET api/<FurnitureController>/5
        [EnableCors]
        [HttpGet("{id}")]
        public string Get(int id) {
            using var connection = new MySqlConnection(Globals.connString);
            connection.Open();

            string query = string.Format("SELECT F.Furniture_Id, F.Furniture_Name, F.Furniture_Height, F.Furniture_Width, F.Furniture_Depth, C.Category_Name FROM Furniture F, Categories C WHERE F.Furniture_Id = {0} AND F.Category_Id = C.Category_Id", id);
            var command = new MySqlCommand(query, connection);
            using var reader = command.ExecuteReader();

            if (reader.Read()) {
                var res = new FurnitureQuery();
                res.ID = (int)reader.GetValue(0);
                res.Name = (string)reader.GetValue(1);
                res.Height = (int)reader.GetValue(2);
                res.Width = (int)reader.GetValue(3);
                res.Depth = (int)reader.GetValue(4);
                res.Category = (string)reader.GetValue(5);

                var dioxcan = JsonConvert.SerializeObject(res);
                connection.Close();

                return dioxcan;
            } else {
                return JsonConvert.SerializeObject("Something is wrong with the query, no data found");
            }
        }
        /*
        [HttpGet("{id}/{date_start}/{date_end}")]
        public string GetPrice(int id, DateTime date_start, DateTime date_end) {
            using var connection = new MySqlConnection(Globals.connString);
            connection.Open();



            
            return JsonConvert.SerializeObject("Something is wrong with the query, no data found");
        }
        */
    }
}
