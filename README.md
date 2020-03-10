# POSM Auth ![CI](https://github.com/posm/posm-auth/workflows/CI/badge.svg)

### Run in Development

```bash
    docker-compose build # docker-compose pull
    docker-compose up
```

- POSM Auth will be avaliable at [localhost:8050](http://localhost:8050)
- Dummy POSM Nginx server will be avaliable at [localhost:8051](http://localhost:8051)
- Initial django super user with credentials (admin:admin123) is created at initial startup.
- Permissions are loaded from [permissions fixture](https://github.com/posm/posm-auth/blob/master/apps/group/fixtures/component_permissions.json) at every container startup.

### NGINX Configuration
- Configuration sample using POSM Auth is here [posm-nginx/posm.conf](https://github.com/posm/posm-auth/blob/master/posm-nginx/posm.conf)


### References
- https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-subrequest-authentication/
- https://developer.okta.com/blog/2018/08/28/nginx-auth-request
