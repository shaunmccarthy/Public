using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Threading;
using System.Web.Http;

namespace AjaxScrollingBug.Controllers
{
    public class ValuesController : ApiController
    {
        public string GetByDelay(string id, int delay)
        {
            Thread.Sleep(delay);
            return id;
        }
    }
}