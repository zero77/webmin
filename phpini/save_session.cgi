#!/usr/local/bin/perl
# Update options related to sessions

require './phpini-lib.pl';
&error_setup($text{'session_err'});
&ReadParse();
&can_php_config($in{'file'}) || &error($text{'list_ecannot'});

&lock_file($in{'file'});
$conf = &get_config($in{'file'});

# Validate and store inputs
&save_directive($conf, "session.save_handler",
		$in{"session.save_handler"});
if ($in{"session.save_path_def"}) {
	&save_directive($conf, "session.save_path", undef);
	}
else {
	if($in{"session.save_handler"} == "redis") {
		my @hasRedis = `php -m | grep redis` == "redis";
		if(!@hasRedis) {
			&error($text{'session_eredis'});
			}
		}
	else {
		# file path must not be checked with other handlers (e.g. redis)
		-d $in{"session.save_path"} || &error($text{'session_epath'});
		}


	&save_directive($conf, "session.save_path",
			$in{"session.save_path"});
	}
&save_directive($conf, "session.use_cookies",
		$in{"session.use_cookies"} || undef);
&save_directive($conf, "session.use_only_cookies",
		$in{"session.use_only_cookies"} || undef);
if ($in{"session.cookie_lifetime_def"}) {
	&save_directive($conf, "session.cookie_lifetime", undef);
	}
else {
	$in{"session.cookie_lifetime"} =~ /^\d+$/ ||
		&error($text{'session_elife'});
	&save_directive($conf, "session.cookie_lifetime",
			$in{"session.cookie_lifetime"});
	}
if ($in{"session.gc_maxlifetime_def"}) {
	&save_directive($conf, "session.gc_maxlifetime", undef);
	}
else {
	$in{"session.gc_maxlifetime"} =~ /^\d+$/ ||
		&error($text{'session_emaxlife'});
	&save_directive($conf, "session.gc_maxlifetime",
			$in{"session.gc_maxlifetime"});
	}

&flush_file_lines_as_user($in{'file'});
&unlock_file($in{'file'});
&graceful_apache_restart($in{'file'});
&webmin_log("session", undef, $in{'file'});

&redirect("list_ini.cgi?file=".&urlize($in{'file'}));

