<%inherit file="${context['logintpl']}" />
<div class="row">
    <div class="${bc['xs']}12">
        <form action="${request.route_url('ppsslogin')}" method="POST" class="loginform">
            
            <input class="form-control" type="text" name="username" placeholder="username" class="form-control">
            <br/>
            <input class="form-control" type="password" name="password" placeholder="password" class="form-control">
            <br/>
            <div class="text-center">
                <input class="btn btn-success" type="submit" name="submit" value="Login"/>
                % if ppsauthconf.newusergroups:
                <br>
                 <small>Not registered yet? <a href="${request.route_url('ppss:user:register')}">Register now</a></small>
                % endif
            </div>
            </br>
            <p class="text-danger">${msg}</p>
        </form>
    </div>
</div>

